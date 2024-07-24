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

texta = '第二十七条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'
textb = '第三十三条　供电企业应当按照国家核准的电价和用电计量装置的记录，向用户计收电费。'

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
