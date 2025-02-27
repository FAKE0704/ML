import os
import PyPDF2
from tqdm import tqdm
from time import sleep
import pandas as pd
from pdfminer.high_level import extract_text
import re
import requests
import json
from pdfplumber import open as pdf_open

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
def call_deepseek_api(pdf_text, question):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'user', 'content': f'参考以下 PDF 文档内容：{pdf_text}\n问题：{question}'}
        ]
    }
    response = requests.post(API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f'API 请求失败，状态码：{response.status_code}'


################################################################
# 配置 API 密钥和 URL
API_KEY = 'your_api_key_here'
API_URL = 'https://api.deepseek.com/v1/chat/completions'

# 配置文件路径
file_path = r"C:\Users\Thomas P Gao\Documents\personal\VSC\VSC_work\work_documents\PWC\Audit Guide" # 请用自己的地址替换
testlist =patch_read_filename(file_path)


# 配置问题
pdf_file_path = 'path_to_your_pdf_file.pdf'
question = '请根据 PDF 文档内容生成审计笔记。'

# 遍历PDF文档，得到文件名testlist; 读取pdf的内容
file_count = 0
for pdffile in testlist:
    if pdffile.endswith('.pdf'):
      file_count += 1
      if file_count == 1:
        print(testlist)
        pdf_text = read_pdf(file_path+"/"+pdffile)


# 调用 DeepSeek AI 模型
notes = call_deepseek_api(pdf_text, question)

 # 输出笔记
print('生成的审计笔记：')
print(notes)



            