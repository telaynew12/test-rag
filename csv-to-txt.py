import os
from pathlib import Path
import pandas as pd
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 1. Read CSV
csv_file = "okr_data.csv"  # your CSV file
df = pd.read_csv(csv_file)

# 2. Combine all rows into one text file
all_content = ""
for idx, row in df.iterrows():
    objective = str(row["objective_name"]).strip()
    keyresults = str(row["keyresults"]).replace("|", "\n")  # split keyresults/milestones
    content = f"Objective {idx+1}: {objective}\n{keyresults}\n\n---\n\n"
    all_content += content

# 3. Save as one .txt file
txt_file = RAW_DIR / "okr_all.txt"
with open(txt_file, "w", encoding="utf-8") as f:
    f.write(all_content)

print(f"✅ Saved all {len(df)} rows into one file: {txt_file}")