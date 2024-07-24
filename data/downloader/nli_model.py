from transformers import AutoModelForSequenceClassification
from transformers import BertTokenizer
import time
import torch
tokenizer=BertTokenizer.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI')
model=AutoModelForSequenceClassification.from_pretrained('IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI')
texta='县级以上地方人民政府经济综合主管部门是本行政区域内的电力管理部门，负责电力事业的监督管理。县级以上地方人民政府有关部门在各自的职责范围内负责电力事业的监督管理。'
textb='县级以上地方人民政府经济综合主管部门是本行政区域内的电力管理部门，负责电力事业的监督管理。县级以上地方人民政府有关部门在各自的职责范围内负责电力事业的监督管理。'
# 开始计时
start_time = time.time()
output=model(torch.tensor([tokenizer.encode(texta,textb)]))
end_conflicts_time = time.time()

print(torch.nn.functional.softmax(output.logits,dim=-1))
print(f"冲突检测时间: {start_time - end_conflicts_time} 秒")