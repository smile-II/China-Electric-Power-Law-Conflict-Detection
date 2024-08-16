
import json
from openai import OpenAI
from tqdm import tqdm 
import concurrent.futures
import yaml
# 加载 YAML 配置文件
with open("D:\project\legal\config\seeting.yml", 'r') as file:
    config = yaml.safe_load(file)
# 访问 secret_key
secret_key = config['secret_key']

# 配置 OpenAI API
client = OpenAI(api_key=secret_key, base_url="https://api.deepseek.com")

def chat_with_model(input_text, temperature=1):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是一个友好的助手。"},
            {"role": "user", "content": input_text}
        ],
        stream=False,
        temperature=temperature,
    )
    return response.choices[0].message.content

# 提取接口返回结果中的选项
def extract_option(answer):
    if 'B' in answer or '最终答案是B' in answer or '答案是B' in answer:
        return 'B'
    elif 'A' in answer or '最终答案是A' in answer or '答案是A' in answer:
        return 'A'
    return "无法确定"

def process_entry(entry):
    input_text = entry['input_title'] + "\n" + entry['input_content']
    retrieved_text = entry['conflict_title'] + "\n" + entry['conflict_content']

    # 定义prompt
    prompt = f"你是一个处理企业合规性的法律专家,请对企业合规性进行分析，分析是否存在法律逻辑上的冲突? 这是企业文本：\n{input_text} 这是法律文本\n{retrieved_text}\n\n##请回答：A：法律文本冲突  B：法律文本不冲突\n##请一步一步思考，然后输出选项A或者B"
    # prompt = f"""
#上下文：你是一个处理企业合规性的法律专家，企业合规性是指企业在其运营和管理过程中，遵守所有适用的法律、法规、行业标准、内部政策以及道德规范的程度。企业合规性的核心目标是确保企业的行为不仅合法，而且符合道德和社会责任的要求，以维护企业的声誉，避免法律风险和经济损失，并促进企业的可持续发展。为了实现这一目标，企业通常会建立并维护一套合规管理体系，涵盖政策制定、合规培训、监控审计、以及违规行为的报告与处理等环节。

#目标：下面请你帮助我进行企业合规性分析。我会给你两段文本，一段是企业规定文本，一段是法律文本，帮助我分析企业规定是否符合法律规定。

#风格：法律专家的语言风格，严谨，保证输出的内容是正确的，没有歧义的。

#语调：书面语调，专业性和技术性的分析。

#受众：分析内容的受众是企业人员，法律专家，输出的内容尽量为人类分析企业合规性提供辅助作用。

#输出：请一步一步思考，输出合规性分析的内容。并且在选项 A：法律文本冲突  B：法律文本不冲突 \n 选择选项A或者B。

#请你对下面两段文本进行企业合规性分析: 企业文本：{input_text}  法律文本：{retrieved_text}
# """

    # 调用API获取回答
    answer = chat_with_model(prompt)

    # 提取选项
    predicted_option = extract_option(answer)

    # 返回处理结果
    return {
        "doc_index": entry['doc_index'],
        "input_title": entry['input_title'],
        "input_content": entry['input_content'],
        "conflict_title": entry['conflict_title'],
        "conflict_content": entry['conflict_content'],
        "confidence": entry['confidence'],
        "answer":answer,
        "result": predicted_option
    }

def main(input_json_path, output_json_path):
    # 读取JSON文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        # 处理文件中的每个 JSON 对象
        data = []
        for line in f:
            data.append(json.loads(line))

    # 准备保存分析结果的列表
    analysis_results = []

    # 使用多线程和进度条进行并发处理
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_entry, entry) for entry in data]
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
            try:
                result = future.result()
                analysis_results.append(result)
            except Exception as e:
                print(f"处理过程中出现错误: {e}")

    # 输出结果到一个新的文件中

    with open(output_json_path, 'a', encoding='utf-8') as f:
        for conflict in analysis_results:
            f.write(json.dumps(conflict, ensure_ascii=False) + '\n')
    # with open(output_json_path, 'w', encoding='utf-8') as f:
    #     json.dump(analysis_results, f, ensure_ascii=False, indent=4)
    print(f"分析结果已保存至 {output_json_path}")

if __name__ == "__main__":
    input_json_path = r'D:\project\legal\output\政策文件_20240813\conflict_results_1.json'  # 输入 JSON 文件路径
    output_json_path = r'D:\project\legal\output\政策文件_20240813\conflict_results_1_stage2-5.json'  # 输出 JSON 文件路径
    main(input_json_path, output_json_path)
