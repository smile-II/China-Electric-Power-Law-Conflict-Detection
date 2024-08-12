from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer
import time
import torch

# 加载模型
tokenizer = BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI')
model = AutoModelForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI')

# 移动模型到GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 条文序号冲突
texta = '第二十七条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'
textb = '第三十三条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'



# 条例名字矛盾
texta = '第一条 根据《电力设施保护条例》（以下简称《条例》），结合本省实际，制定本办法。'
textb = '第一条 根据《中华人民共和国电力法》，结合本省实际，制定本办法。'

# 条例名字矛盾
texta = '第三十六条 实施行政处罚时，应当按照《中华人民共和国行政处罚法》的规定执行。'
textb = '第四十七条\n违反本条例规定的行为，本条例未设定处罚但其他法律法规已设定处罚规定的，依照有关法律法规的规定处罚。'


# 关键词矛盾
texta = '第二十条\n违反本条例第十条规定，施工作业单位对电力设施造成损害未停止作业的，由市电力主管部门责令停止作业，恢复原状，并赔偿损失。'
textb = '第四十条 违反本条例第二十七条规定，未经批准、未签订协议擅自施工的，由电力管理部门责令停止作业、恢复原状并赔偿损失。'

# 编码文本并移动到GPU
inputs = tokenizer.encode_plus(texta, textb, return_tensors='pt')
inputs = {key: value.to(device) for key, value in inputs.items()}

# 开始计时
start_time = time.time()
with torch.no_grad():  # 禁用梯度计算，加速推理
    output = model(**inputs)
end_conflicts_time = time.time()

# 计算 softmax
probs = torch.nn.functional.softmax(output.logits, dim=-1)

print(probs)
print(f"冲突检测时间: {end_conflicts_time - start_time} 秒")
