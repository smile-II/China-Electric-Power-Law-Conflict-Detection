import requests
import pyarrow.parquet as pq
import json
from pathlib import Path

def download_and_convert_to_json(dataset_url):
    # 获取所有文件的链接
    response = requests.get(dataset_url)
    response.raise_for_status()
    files = response.json()

    for file in files:
        file_url = f"{dataset_url.rstrip('/')}/{file['path']}"
        file_name = file['path']

        # 下载文件
        file_response = requests.get(file_url)
        file_response.raise_for_status()

        # 保存文件到本地
        with open(file_name, "wb") as local_file:
            local_file.write(file_response.content)

        # 检查文件扩展名是否为 parquet
        if file_name.endswith('.parquet'):
            # 读取 Parquet 文件
            table = pq.read_table(file_name)

            # 将数据转换为 JSON 格式
            json_data = table.to_pylist()

            # 保存 JSON 数据到文件
            json_file_name = Path(file_name).stem + '.json'
            with open(json_file_name, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            print(f"文件 {file_name} 已成功转换为 JSON 格式并保存为 {json_file_name}")

# 使用示例
dataset_url = "https://huggingface.co/datasets/twang2218/chinese-law-and-regulations/tree/main"
download_and_convert_to_json(dataset_url)