import os
import json
import shutil
import nltk
from tqdm import tqdm
from chains.local_doc_qa import LocalDocQA
from configs.model_config import *
import models.shared as shared
from models.loader.args import parser
from models.loader import LoaderCheckPoint

nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path

def init_model():
    args = parser.parse_args()
    args_dict = vars(args)
    shared.loaderCheckPoint = LoaderCheckPoint(args_dict)
    llm_model_ins = shared.loaderLLM()
    llm_model_ins.history_len = LLM_HISTORY_LEN
    local_doc_qa = LocalDocQA()
    try:
        local_doc_qa.init_cfg(llm_model=llm_model_ins)
        print("模型已成功加载，可以开始对话")
        return local_doc_qa
    except Exception as e:
        print(f"模型加载失败: {e}")
        return None

def get_answer(local_doc_qa, query, history, streaming=False):
    answer_result_stream_result = local_doc_qa.llm_model_chain(
        {"prompt": query, "history": history, "streaming": streaming})
    
    answers = []
    for answer_result in answer_result_stream_result['answer_result_stream']:
        resp = answer_result.llm_output["answer"]
        history = answer_result.history
        answers.append(resp)
    
    return answers, history

def extract_option(answers):
    predicted_option = None
    for answer in reversed(answers):
        if 'B' in answer or '最终答案是B' in answer or '答案是B' in answer:
            predicted_option = 'B'
            break
        elif 'A' in answer or '最终答案是A' in answer or '答案是A' in answer:
            predicted_option = 'A'
            break
    return predicted_option

def main(input_json_path, output_json_path):
    # 初始化模型
    local_doc_qa = init_model()
    if not local_doc_qa:
        return

    history = []

    # 读取输入的 JSON 文件
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = []

    # 使用tqdm显示进度条
    with tqdm(total=len(data), desc="Processing") as pbar:
        for entry in data:
            doc_index = entry["doc_index"]
            input_text = entry["conflict"]["input_text"]
            retrieved_text = entry["conflict"]["retrieved_text"]
            label = entry["conflict"]["label"]
            confidence = entry["conflict"]["confidence"]
            
            prompt = f"这两条法律是否存在法律逻辑上的冲突?\n{input_text}\n{retrieved_text}\n\n##请回答：A：法律文本冲突  B：法律文本不冲突\n##请一步一步思考，然后输出选项A或者B"
            answers, history = get_answer(local_doc_qa, prompt, history)

            # 提取选项
            predicted_option = extract_option(answers)

            result = {
                "doc_index": doc_index,
                "conflict": {
                    "input_text": input_text,
                    "retrieved_index": entry["conflict"]["retrieved_index"],
                    "retrieved_text": retrieved_text,
                    "label": label,
                    "confidence": confidence
                },
                "predicted_option": predicted_option,
                "answers": answers
            }

            results.append(result)

            # 实时保存结果到 JSON 文件
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

            pbar.update(1)

if __name__ == "__main__":
    input_json_path = '/home/txs/work/sjl/Langchain-Chatchat-0.1.17/detect_conflict_stage_2/data/conflict_results-1.json'  # 输入 JSON 文件路径
    output_json_path = '/home/txs/work/sjl/Langchain-Chatchat-0.1.17/detect_conflict_stage_2/output/conflict_results-2.json'  # 输出 JSON 文件路径
    main(input_json_path, output_json_path)
