from openai import OpenAI
client = OpenAI(api_key="sk-9a58fb2932634704bac709c2dc26ab50", base_url="https://api.deepseek.com")
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
from concurrent.futures import ThreadPoolExecutor

def chat_with_model(input_text, temperature=1.25):
    # 调用OpenAI API的chat接口
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

def extract_text_from_resume(resume):
    text = ""
    for key, value in resume.items():
        if isinstance(value, dict):
            text += " ".join(str(v) for v in value.values())
        elif isinstance(value, list):
            text += " ".join(value)
    return text


# 检查文本相似性的函数
def check_resume_similarity(new_resume, resume_database, threshold=0.7):
    """_summary_

    Args:
        new_resume (_type_): _description_
        resume_database (_type_): _description_
        threshold (float, optional): _description_. Defaults to 0.7.

    Returns:
        bool: _description_
    """
    # 确保简历数据库和新简历都是有效的
    if not new_resume or not resume_database:
        return True #如果库是空的直接添加
    
    # 提取所有简历的文本
    if resume_database:
        resume_texts = [extract_text_from_resume(resume) for resume in resume_database]
    else:
        resume_texts = []

    # 提取新简历的文本
    new_resume_text = extract_text_from_resume(new_resume)

    # 将新简历的文本添加到列表中
    resume_texts.append(new_resume_text)

    # 使用TF-IDF向量化器将文本转换为向量
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(resume_texts)

    # 计算新简历向量与简历库中每个简历向量之间的余弦相似度
    cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])

    # 打印相似度结果
    for i, similarity in enumerate(cosine_similarities[0]):
        print(f"新简历与简历{i+1}的相似度为: {similarity}")

    # 如果您想检查相似度是否超过某个阈值
    threshold = threshold
    if any(similarity >= threshold for similarity in cosine_similarities[0]):
        return False  # 新简历与简历库中的某个简历过于相似！
    else:
        return True  # 新简历可以加入到简历库中。
    # json_list = [{"基本信息": {"姓名": "张强", ...}, ...}, ...]
    # new_resume = json_list[9]  # 假设第10个简历是新简历
    # if check_resume_similarity(new_resume, json_list):
    #     print("新简历可以加入到简历库中。")
    # else:
    #     print("新简历与简历库中的某个简历过于相似！")


# 定义一个函数来生成指定数量的简历数据字符串
def generate_resume_data(dataset, num_samples=3):
    """_summary_
    假设这是你的结果列表
    results = ['样本1', '样本2', '样本3', '样本4', '样本5']

    # 生成4个简历数据字符串
    print(generate_resume_data(results,3))
    """
    # 计算数据库中的示例数量
    num_elements = len(dataset)
    
    # 如果示例数量小于或等于num_samples，则返回所有示例
    if num_elements <= num_samples:
        random_samples = dataset
    else:
        # 如果示例数量大于num_samples，则随机选择num_samples个示例
        random_samples = random.sample(dataset, num_samples)

    # 创建一个字符串列表来存储简历数据
    resume_data_list = []

    # 使用循环构建每个简历数据的字符串
    for i, sample in enumerate(random_samples, start=1):
        resume_data_list.append(f"匹配的简历数据{i}：\n{sample}\n")

    # 将列表转换为字符串
    resume_data_str = "\n".join(resume_data_list)

    return resume_data_str

def process_job_description(job_info_str, resume_pool, i):
    while len(resume_pool) < 100:
        # 获取随机示例
        random_samples = generate_resume_data(resume_pool,3)      
        prompt = f"""
        #上下文：我想制作一个简历数据集，这个数据集分为岗位描述和简历数据两部分。我会给你岗位描述部分，请你帮我生成与岗位描述匹配的简历数据部分。
        #目标：根据提供的岗位描述，生成匹配的简历。
        <岗位描述的关键字段>
        岗位名称，岗位职责，岗位要求

        <简历数据的关键字段>
        基本信息：姓名，年龄，性别，身高，体重
        教育经历：学校，学历，专业，GPA排名，主修课程，学校层次
        技能：专业技能，其他技能
        实习经历：实习公司，实习时间、地点，实习描述
        项目经历：项目名称、时间、地点，项目描述
        其他经历：获得荣誉，语言水平，自我评价

        我会给出岗位描述关键字段的内容，请你模仿求职者，尽你最大的能力，充分填写简历数据内容，你对这份简历非常的重视！

        #风格：简历书写风格，但是内容详细。为了保证简历数据的多样性，请你尽可能的模仿不同学校，不同专业，不同项目经历的求职者，并且保证你的简历信息是真实的，你输出的简历信息是符合现实世界的数据分布的。
        #语调：书面语调，专业性和技术性，内容丰富，模拟真实世界中的多样化场景。

        #受众：简历的受众主要是面试官，针对这一群体，尽量展示自己的亮点，以及对这个岗位的需求。

        ###下面是一个岗位描述和匹配的简历数据的示例###：
        <岗位描述>
        {job_info_str}

        <匹配的简历数据>
        {random_samples}

        ###开始生成简历数据###
        #响应要求：
        1.回复仅仅输出一个简历数据json格式，不要输出jsons格式之外的任何内容。
        2.给你的岗位描述就是示例中的岗位描述。
        3.你生成的简历数据关键字段的内容不能和示例中的简历数据关键字段的内容相同。
        4.请你在匹配岗位描述的情况下尽可能的生成内容多样的简历。
        <请你生成的匹配岗位描述的简历数据如下:>
        """
        

        # 调用LLM接口
        llm_response = chat_with_model(prompt)
        # 尝试提取JSON字符串
        try:
            # 使用maxsplit参数确保只分割一次
            parts = llm_response.split("```json", 1)
            # 再次分割，确保后面有"```"
            json_parts = parts[1].split("```", 1)
            # 提取JSON字符串并去除前后空白
            json_str = json_parts[0].strip()
            # 解析JSON字符串
            resume = json.loads(json_str)
        except IndexError:
            print("No JSON found in the response. Skipping JSON parsing.")
            resume = None  # 或者你可以设置一个默认值
        
        # 检查生成的文本与数据库中文本的相似性
        if resume is not None and check_resume_similarity(resume, resume_pool):
            resume_pool.append(resume)
        else:
            print("新简历与简历库中的某个简历过于相似！")
        
        file_name = f'D:\project\FUZZYLORA\data_gen\output_batch\jd_id_{i}.jsonl'
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
            
        with open(file_name, 'a', encoding='utf-8') as f:
                json_str = json.dumps(resume, ensure_ascii=False, indent=4) 
                f.write(json_str + '\n')
        
        if len(resume_pool) >= 100:
            print("简历池已达到100份，停止生成简历。")
            break


def main():
    df = pd.read_excel('D:\project\FUZZYLORA\data_gen\job_description_20.xlsx')
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # 设置线程数为5
        for i in range(len(df)):
            job_info_str = f"""
            岗位名称：{df["岗位名称"][i]}
            岗位职责：{df["岗位职责"][i]}
            岗位要求：{df["岗位要求"][i]}
            """
            resume_pool = []  # 每个线程有自己的简历池
            executor.submit(process_job_description, job_info_str, resume_pool, i)

if __name__ == "__main__":
    main()    
    


