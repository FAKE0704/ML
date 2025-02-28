import os
import PyPDF2
from openai import OpenAI
from tqdm import tqdm
from time import sleep
import pandas as pd
from pdfminer.high_level import extract_text
import re
import requests
import json
from pdfplumber import open as pdf_open
from datetime import datetime

def patch_read_filename(filePath):
    """
    获取目标路径的文件名称
    """
    nameList = os.listdir(filePath)
    names= globals()
    count=0

    # 初始化一个空列表来存储文件名
    file_list = []

    # 遍历文件夹
    for filename in os.listdir(filePath):
        file_list.append(filename)

    # 输出文件名列表
    return file_list


# 读取 PDF 文档
def read_pdf(file_path):
    with pdf_open(file_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text


# 调用 DeepSeek AI 模型
def talk_base_AI(API_KEY, model, role, question):
    client = OpenAI(
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
        api_key=API_KEY, # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 调用AI 模型
    completion = client.chat.completions.create(
        model=model, 
        messages=[
            {'role': 'system', 'content': role},
            {'role': 'user', 'content': question}
            ],
        timeout=280
    )

    return completion.choices[0].message.content

def talk_file_AI(API_KEY, model, role, question,pdf_text,requirements):
    question = f'请参考以下内容：{pdf_text}\n question \n 要求:{requirements}'
    return talk_base_AI(API_KEY, model, role, question)


################################################################
# 配置 API 密钥和 URL
# API_URL = 'https://dashscope.aliyuncs.com/api/v1/'
API_KEY = 'sk-4e28a0f9c9064576895552d2bb361f48'
model="deepseek-v3" # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models

# 配置文件路径
file_path = r"C:\Users\Thomas P Gao\Documents\personal\VSC\VSC_work\work_documents\PWC\Audit Guide" # 请用自己的地址替换
testlist =patch_read_filename(file_path)

#-----------TASK1：PDF文件内容提取----------------
# 设置ai的角色
role = '你是一名审计专家'
question = '生成markdown格式的审计笔记。'
requirements = "1.PDF中的文字不能够做增或者减,如果是冗余空格则可以删除；2.选择合适的行作为一级标题、二级标题;3.如果遇到流程图或者表格,请使用mermaid或者markdown语法进行描述。"


# 遍历PDF文档，得到文件名testlist; 读取pdf的内容
file_count = 0
for pdffile in testlist:
    if pdffile.endswith('.pdf'):
      file_count += 1
      if file_count == 1:
        print(pdffile)
        pdf_text = read_pdf(file_path+"/"+pdffile)
        if len(pdf_text) >=  57344:
            print(f'PDF文件{pdffile}的内容长度为{len(pdf_text)}，超过{model}模型的限制，正在分批处理...')
            # 按章节标题分块
            chunks = []
            current_chunk = []
            for line in pdf_text.split('\n') : # 如果分割
                if line.startswith(r'^\d+(?:\.\d+)+$'):
                    if current_chunk:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = []
                else:
                    print(line)
                current_chunk.append(line)
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            print(len(chunks))
            
            content = ''
            for i, chunk in enumerate(chunks):
                # 先只运行第一块
                # if i not in range(3) and i < 6:
                if i in range(1) and i < 6:
                    print(f'正在处理第{i+1}块,长度为{len(chunk)}...')
                    current_time = datetime.now()
                    current_content = talk_file_AI(API_KEY, model, role, question,chunk,requirements)
                    content =content+"\n"+ current_content
                    cost_time = datetime.now() - current_time
                    print(f'第{i+1}块处理完成，耗时{cost_time}')
            # 创建并写入到文件
            with open(r"C:\Users\Thomas P Gao\Documents\personal\VSC\VSC_work\work_documents\PWC\Audit Guide\output.md", "w", encoding="utf-8") as file:
                file.write(content)

            print(f"文件已成功创建并写入")
        else:
            pass
            # 输出笔记
            # content = talk_file_AI(API_KEY, model, role, question,pdf_text,requirements)
            # type(content)
            # print('生成的内容：')
            # print(content)
