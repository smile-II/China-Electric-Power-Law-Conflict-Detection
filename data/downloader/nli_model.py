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

# texta = '第二十七条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'
# textb = '第三十三条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'
# 这居然是矛盾的，删除 第二十七条 这种文本


# texta = '供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'
# textb = '用户应当按照用电计量装置的计量值及时足额缴纳电费，不得危害供用电安全和扰乱供用电秩序。'
# 中立

# texta = '事故造成地铁、机场、高层建筑、商场、影剧院、体育场馆等人员聚集场所停电的，应当迅速启用应急照明，组织人员有序疏散。'
# textb = '遇到危害电力设施安全或者严重妨碍电力设施抢修的情形，有关部门及电力企业应当及时制止。必要时电力企业可以采取中止供电等措施，确保及时抢修损坏的电力设施。'
# 矛盾


texta = '第三十八条　违反本条例规定，有下列行为之一的，由电力管理部门责令改正，没收违法所得，可以并处违法所得5倍以下的罚款：(一)事故发生的时间、地点(区域)以及事故发生单位；'
textb = '这是一条完整的，逻辑清晰的法律条例'



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
