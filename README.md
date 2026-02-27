# GitTaskBench Reproduction: Eparse_01 (Windows)

## 1. Project summary
This repository contains my reproducibility run for **GitTaskBench** on a single task **Eparse_01** (Excel parsing → formatted text output).  
I verify the result using the official evaluation command:

- `gittaskbench grade --taskid Eparse_01`
- Status: **PASSED**
- Final score: **75.00%** (threshold = 75%)

Included artifacts:
- `output.txt` (prediction output)
- `results.jsonl` (official evaluation output)
- `process_excel_to_txt.py` (script used to generate `output.txt`)
- `grade_pass.png` (screenshot of PASS)
- `gt.txt` (ground truth used by the official evaluator for Eparse_01) 

---

## 2. Reproduction target (metric)
**Target claim:** Task **Eparse_01** passes the official evaluation (PASS/FAIL + final score).  
**Metric:** `final_score = 0.3 * filename_match + 0.7 * content_similarity`, PASS if `final_score >= 0.75`.

---

## 3. Environment
- OS: Windows
- Python: 3.11
- GitTaskBench root (local): `D:\projects\GitTaskBench`
- Eparse repo (local): `D:\projects\GitTaskBench\code_base\Eparse`
- Input directory: `D:\projects\GitTaskBench\queries\Eparse_01\input\Eparse_01_input\`
- Output file: `D:\projects\GitTaskBench\output\Eparse_01\output.txt`

**No API keys are included in this repo.**

---

## 4. How to reproduce (step-by-step)

### Step A: Install Python dependencies
Run in Git Bash / Anaconda Prompt:

```bash
python3 -m pip install openpyxl pandas
```

### Step B: Set PYTHONPATH so Python can import eparse

Run in Git Bash:
```bash
export PYTHONPATH="D:\\projects\\GitTaskBench\\code_base\\Eparse"
export PYTHONPATH="D:\\projects\\GitTaskBench\\code_base\\Eparse"
```
### Step C: Generate prediction output

Run:
```bash
python3 D:/projects/GitTaskBench/prompt/Eparse_01/process_excel_to_txt.py
```
This reads inputs from:
```
D:\projects\GitTaskBench\queries\Eparse_01\input\Eparse_01_input\
```
and writes:
```
D:\projects\GitTaskBench\output\Eparse_01\output.txt
```
### Step D: Grade (official evaluation)

In Anaconda Prompt (inside env gtb), run:
```
cd /d D:\projects\GitTaskBench
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
gittaskbench grade --taskid Eparse_01
```
Expected:

Status: PASSED

## 5. Modification(s)

Small but meaningful changes required to reproduce on my setup:

Installed missing dependency openpyxl (required by eparse.core for Excel parsing).

Updated the parsing script to handle get_df_from_file return format differences (tuple vs dict).

Fixed Windows evaluation printing issue by forcing UTF-8 output (PYTHONIOENCODING=utf-8, PYTHONUTF8=1).


## 6. Results (official output summary)

From gittaskbench grade --taskid Eparse_01:

Filename match rate: 100%

Content similarity:

table_date.xlsx: 85.71%

table_epa.xlsx: 42.86%

Average content similarity: 64.29%

Final score: 75.00%

Status: PASSED

Detailed evaluation is in results.jsonl.


## 7. Artifacts included

process_excel_to_txt.py (script used to generate the prediction output)

output.txt (prediction output for Eparse_01)

results.jsonl (official evaluation output saved by GitTaskBench)

gt.txt (ground truth file used by the official evaluator for Eparse_01)

grade_pass.png (screenshot showing Status: PASSED)



