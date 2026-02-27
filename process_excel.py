import os
from pathlib import Path
import pandas as pd
# 假设 eparse.core.get_df_from_file 存在并按描述工作
# from eparse.core import get_df_from_file # 假设此处能够正确导入

# 定义路径
GIT_ROOT = Path(r"D:\projects\GitTaskBench")
INPUT_DIR = GIT_ROOT / "queries" / "Eparse_01" / "input" / "Eparse_01_input"
OUTPUT_FILE = GIT_ROOT / "output" / "Eparse_01" / "output.txt"

# 确保输出目录存在
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

all_output_blocks = []

# 处理输入目录中的每个 Excel 文件
# 假设 Excel 文件为 .xlsx 格式
for excel_file_path in INPUT_DIR.glob("*.xlsx"):
    file_output_blocks = []
    file_output_blocks.append(f"文件名: {excel_file_path.name}")

    try:
        # 使用 eparse.core.get_df_from_file 解析 Excel 文件
        # 假设它返回一个 {sheet_name: DataFrame} 的字典
        # 或者在返回单个 DataFrame 时，我们将其包装成字典
        # 注意：此处使用 pd.read_excel 作为 get_df_from_file 的占位符，因为实际的 eparse.core.get_df_from_file 未提供。
        # 实际部署时应替换为 from eparse.core import get_df_from_file 并调用 get_df_from_file(str(excel_file_path))
        # 假定 get_df_from_file 行为类似于 pd.read_excel(sheet_name=None)
        dataframes_by_sheet = pd.read_excel(str(excel_file_path), sheet_name=None)
        
        # 如果 get_df_from_file 返回的不是字典（例如，是单个 DataFrame），则进行包装
        if not isinstance(dataframes_by_sheet, dict):
            dataframes_by_sheet = {"Sheet1": dataframes_by_sheet} # 使用"Sheet1"作为默认工作表名

    except Exception as e:
        file_output_blocks.append(f"Error parsing file {excel_file_path.name}: {e}")
        all_output_blocks.extend(file_output_blocks)
        all_output_blocks.append("") # 错误文件后也加空行
        continue

    for sheet_name, df in dataframes_by_sheet.items():
        file_output_blocks.append(f"    Sheet: {sheet_name}")
        # 将 DataFrame 转换为字符串，不包含索引，以匹配 gt.txt 样式
        # df.to_string() 默认包含列头
        file_output_blocks.append(df.to_string(index=False))

    all_output_blocks.extend(file_output_blocks)
    all_output_blocks.append("") # 每个文件块之间添加空行，以提高可读性，并模拟gt.txt的可能格式

# 拼接所有块并写入输出文件
# .strip() 用于移除末尾可能的多余空行
final_output_content = "\n".join(all_output_blocks).strip()
OUTPUT_FILE.write_text(final_output_content, encoding='utf-8') # 明确指定编码，防止中文乱码

print(f"Prediction output generated at: {OUTPUT_FILE}")
