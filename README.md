# FTEC5660 Individual Project — Reproduction: GitTaskBench (Eparse_01)

**Name:** Ruiqian Luo  
**Student ID:** 1155244663  
**Course:** FTEC5660  

## 1. Project summary

This project reproduces a small, clearly-defined evaluation task from **GitTaskBench**: **Eparse_01**.

**Target claim (reproduction target):**  
I reproduce the official GitTaskBench grader result for task **Eparse_01** (i.e., the grader output and final score based on filename match + content similarity).

In this task, the goal is to generate a prediction file (`output.txt`) that contains parsed Excel table blocks in the expected text format, then run the official evaluation script via `gittaskbench grade`.

## 2. What Eparse_01 does

Eparse_01 is an *Excel parsing / table extraction* task inside GitTaskBench.  
Given the provided Excel files under the task input folder, the system should output a text file containing:

- Each Excel filename
- Each sheet name
- A plain-text table representation (DataFrame-like) of the extracted content

The official grader compares the **prediction output** against a **ground truth** text file using:
- **Filename match**
- **Content similarity** (per-file similarity + average similarity)
- A weighted final score and a pass threshold

## 3. Environment

- OS: Windows
- Python environment: Conda env `gtb`
- Hardware: Local laptop GPU (RTX 5070 Ti)
- Note: The reproduction and grading steps were run locally.

## 4. How to reproduce (step-by-step)

### Step A — Install Python dependencies

Run in **Anaconda Prompt** (inside env `gtb`) or Git Bash:

```bat
python -m pip install --upgrade pip
python -m pip install openpyxl pandas
```

### Step B: Set PYTHONPATH so Python can import eparse
You need Python to import eparse from the included repo copy:
Run in Git Bash:
Option 1 (Anaconda Prompt / Windows CMD):

```bash
set PYTHONPATH=D:\projects\GitTaskBench\code_base\Eparse
```
Option 2 (Git bash)
```
export PYTHONPATH="/d/projects/GitTaskBench/code_base/Eparse"
```
### Step C: Generate prediction output
Run the task script to generate:

Input: D:\projects\GitTaskBench\queries\Eparse_01\input\Eparse_01_input\

Output: D:\projects\GitTaskBench\output\Eparse_01\output.txt

Command:
Run:

```bash
cd /d D:\projects\GitTaskBench
python prompt\Eparse_01\process_excel.py
```

After running, confirm the output exists:

```bash
dir output\Eparse_01\output.txt
```

### Step D: Grade (official evaluation)
On Windows, the evaluation script may fail to print JSON under a non-UTF8 console encoding.
To avoid encoding errors, force UTF-8:

```bash
cd /d D:\projects\GitTaskBench
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
gittaskbench grade --taskid Eparse_01
```

Expected:

Status: PASSED

## 5. Modification(s)

Small but meaningful changes required to reproduce on my setup:

Installed missing dependency openpyxl
Required by eparse.core to parse Excel files.

Updated the task script output formatting to match the ground truth structure
I adjusted the output format (file/sheet headers + DataFrame printing) so the grader can recognize Excel data blocks correctly.

Fixed Windows evaluation printing issue by forcing UTF-8 output
Setting:

PYTHONIOENCODING=utf-8

PYTHONUTF8=1
prevents UnicodeEncodeError during grader JSON printing.


## 6. Results (official output summary)


From 

```bash
gittaskbench grade --taskid Eparse_01:
```
Official summary:

Filename match rate: 100.00%

Content similarity:

table_date.xlsx: 100.00%

table_epa.xlsx: 66.67%

Average content similarity: 83.33%

Final score (filename match 30% + content similarity 70%): 88.33%

Status: PASSED

Detailed evaluation output:

results.jsonl


## 7. Artifacts included

This repo includes the following artifacts for verification:

process_excel_to_txt.py (script used during development / parsing)

output.txt (prediction output for Eparse_01)

results.jsonl (official grader result log)

grade_pass.png (screenshot proof of PASS)

Notes:

Ground truth is part of the original GitTaskBench task files (not produced by my script).

---

```markdown
# agent_notes.md — Agentic workflow / debug diary (Eparse_01)

This document records how an agentic workflow was used to reach a passing, reproducible result.

## Summary

I used an LLM-assisted agent workflow (Aider + Gemini API) to:
- inspect the GitTaskBench repository structure,
- locate the correct task files and expected format,
- iteratively adjust the parsing/output script,
- resolve environment and Windows encoding issues,
until the official grader reported **Status: PASSED**.

## Key blockers encountered

### 1) Repo / task wiring issues
- Initially, the grader reported missing output directories or “no valid .md tasks” due to incorrect prompt directory paths and missing generated prompts.
- I located where GitTaskBench stores prompts and ensured the correct task prompt files existed before running any batch scripts.

### 2) Windows console encoding caused grader failure
- The evaluation script printed JSON with symbols that failed under the default Windows console encoding (e.g., GBK).
- Fix: force UTF-8 output using:
  - `PYTHONIOENCODING=utf-8`
  - `PYTHONUTF8=1`

### 3) Dependency + import issues for Excel parsing
- Import errors occurred when the environment lacked `openpyxl`, and when `PYTHONPATH` did not include the local `Eparse` repo path.
- Fix: install missing packages and set `PYTHONPATH` appropriately.

### 4) Output-format mismatch (“0 Excel data blocks found”)
- At one point the grader reported:
  - “Prediction file contains 0 Excel data blocks”
  while the ground truth contained 2 blocks.
- Root cause: the prediction file’s block delimiters / headers did not match what the grader expects.
- Fix: adjust the output format to match the ground truth structure:
  - include file header blocks,
  - include sheet header lines,
  - print DataFrame content in the expected plain-text style.

## What makes this “agentic” (not just a single script run)

The workflow included multiple-step planning + tool-use loops:
- the agent navigated a large repo, identified task-specific folders, and mapped the evaluation pipeline,
- it proposed concrete edits to scripts and configuration (formatting/paths/encoding),
- I executed the proposed changes locally and fed the observed failures back into the loop,
- we iterated until the official evaluation passed.
```
## Final outcome

After applying the fixes above, running the official evaluation:

```
gittaskbench grade --taskid Eparse_01

produced:

Final score: 88.33%

Status: PASSED

Results saved in: results.jsonl

(See grade_pass.png for screenshot evidence.)
```
