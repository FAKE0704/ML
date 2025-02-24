import os
import PyPDF2
from pdfminer.high_level import extract_text

def process_pdf(a):
    try:
        # 1. 在a的路径创建一个文件夹，命名为k
        directory, _ = os.path.split(a)
        k_folder = os.path.join(directory, 'k')
        os.makedirs(k_folder, exist_ok=True)

        # 2. 取PDF文件名的第二个字符到符号"-"前的所有字符作为k1
        filename = os.path.basename(a)
        name_part = filename.split('.')[0]  # 去掉扩展名
        if '-' not in name_part:
            raise ValueError("PDF文件名中没有找到'-'字符")
        second_char_index = 1
        k1 = name_part[second_char_index : name_part.index('-')]

        # 3. 扫描PDF的文字，取"行程时间："后该行的所有字符作为date
        text = extract_text(a)
        lines = text.split('\n')
        date = None
        for line in lines:
            if "行程时间：" in line:
                date = line.split("行程时间：")[1].strip()
                break

        # 4. k = k1 + date
        k = f"{k1}_{date}"

        print(f"k: {k}")
        print(f"k1: {k1}")
        print(f"date: {date}")

    except Exception as e:
        print(f"发生错误: {e}")

# 示例使用
a = "C:/Users/Thomas P Gao/Documents/personal/报销/hfy/test/【享道出行-100.42元-3个行程】高德打车电子行程单.pdf"
process_pdf(a)
