import os
import pandas as pd
from typing import List, Dict, Any

# 在运行此脚本之前，必须将 Eparse 仓库的根目录添加到 PYTHONPATH 环境变量中。
# 例如，在您的终端中运行以下命令：
# Linux/macOS: export PYTHONPATH="$PYTHONPATH:D:\projects\GitTaskBench\code_base\Eparse"
# Windows Command Prompt: set PYTHONPATH=%PYTHONPATH%;D:\projects\GitTaskBench\code_base\Eparse
# Windows PowerShell: $env:PYTHONPATH = "$env:PYTHONPATH;D:\projects\GitTaskBench\code_base\Eparse"
try:
    from eparse.core import get_df_from_file
except ImportError:
    print("错误: 无法导入 'eparse.core.get_df_from_file'。")
    print("请确保 Eparse 仓库的根目录已添加到您的 PYTHONPATH 环境变量中。")
    print("例如 (Linux/macOS): export PYTHONPATH=\"$PYTHONPATH:D:\\projects\\GitTaskBench\\code_base\\Eparse\"")
    print("例如 (Windows CMD): set PYTHONPATH=%PYTHONPATH%;D:\\projects\\GitTaskBench\\code_base\\Eparse")
    print("例如 (Windows PowerShell): $env:PYTHONPATH = \"$env:PYTHONPATH;D:\\projects\\GitTaskBench\\code_base\\Eparse\"")
    exit(1)

def process_excel_files_to_txt(input_dir: str, output_file_path: str):
    """
    遍历指定目录下的所有Excel文件，提取每个文件中各个工作表的内容，
    并以DataFrame样式格式化输出到指定的文本文件。

    Args:
        input_dir (str): 包含Excel文件的输入目录的绝对路径。
        output_file_path (str): 输出文本文件的绝对路径。
    """
    # 确保输出目录存在
    output_dir = os.path.dirname(output_file_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(input_dir):
            for file in files:
                # 检查文件是否为 Excel 文件（.xlsx 或 .xls）
                if file.endswith(('.xlsx', '.xls')):
                    excel_file_path = os.path.join(root, file)
                    outfile.write(f"文件名: {file}\n")
                    outfile.write("=" * 80 + "\n\n") # 文件分隔符

                    try:
                        # 使用 eparse.core.get_df_from_file 读取 Excel 文件。
                        # 如果未指定 'sheet' 参数，它将尝试处理所有工作表。
                        tables_data: List[Dict[str, Any]] = get_df_from_file(io=excel_file_path)

                        if not tables_data:
                            outfile.write(f"  - 文件 '{file}' 中未找到可解析的表格或工作表。\n\n")
                            continue

                        for i, table_info in enumerate(tables_data):
                            df = None
                            sheet_name = f"未知工作表_{i+1}"

                            if isinstance(table_info, dict):
                                df = table_info.get("data")
                                sheet_name = table_info.get("sheet", sheet_name)
                            elif isinstance(table_info, (tuple, list)):
                                if len(table_info) >= 2:
                                    a, b = table_info[0], table_info[1]
                                    if hasattr(a, "to_string") and not hasattr(b, "to_string"):
                                        df = a
                                        sheet_name = str(b)
                                    elif hasattr(b, "to_string") and not hasattr(a, "to_string"):
                                        sheet_name = str(a)
                                        df = b
                                    else:
                                        sheet_name = str(a)
                                        df = b
                                elif len(table_info) == 1:
                                    df = table_info[0]
                            elif hasattr(table_info, "to_string"):
                                df = table_info


                            if df is not None and not df.empty:
                                outfile.write(f"工作表: {sheet_name}\n")
                                outfile.write("-" * 60 + "\n") # 工作表分隔符
                                # 将 DataFrame 格式化为字符串，包含表头，不包含索引
                                outfile.write(df.to_string(index=False) + "\n\n")
                            else:
                                outfile.write(f"  - 工作表 '{sheet_name}' 为空或无法解析。\n\n")
                    except Exception as e:
                        outfile.write(f"  - 处理文件 '{file}' 时发生错误: {e}\n\n")
                    outfile.write("\n") # 每个文件内容后添加额外空行

if __name__ == '__main__':
    # 定义输入Excel文件目录的绝对路径
    INPUT_EXCEL_DIR = r"D:\projects\GitTaskBench\queries\Eparse_01\input\Eparse_01_input"
    # 定义输出文本文件的绝对路径
    OUTPUT_TEXT_FILE = r"D:\projects\GitTaskBench\output\Eparse_01\output.txt"
    # Eparse 仓库的绝对路径，用于指导用户设置 PYTHONPATH
    EPARSE_REPO_PATH = r"D:\projects\GitTaskBench\code_base\Eparse"

    print(f"请确保 Eparse 仓库路径已添加到 PYTHONPATH 环境变量中：")
    print(f"  Linux/macOS: export PYTHONPATH=\"$PYTHONPATH:{EPARSE_REPO_PATH}\"")
    print(f"  Windows CMD: set PYTHONPATH=%PYTHONPATH%;{EPARSE_REPO_PATH}")
    print(f"  Windows PowerShell: $env:PYTHONPATH = \"$env:PYTHONPATH;{EPARSE_REPO_PATH}\"")
    print("-" * 80)

    print(f"开始处理Excel文件，输入目录: {INPUT_EXCEL_DIR}")
    print(f"结果将写入: {OUTPUT_TEXT_FILE}")
    process_excel_files_to_txt(INPUT_EXCEL_DIR, OUTPUT_TEXT_FILE)
    print("处理完成。")
