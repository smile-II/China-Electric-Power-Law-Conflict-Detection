from transformers import AutoModelForSequenceClassification

# 加载模型
model_name = 'IDEA-CCNL/Erlangshen-MegatronBert-1.3B-NLI'
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 打印模型的结构
print(model)
