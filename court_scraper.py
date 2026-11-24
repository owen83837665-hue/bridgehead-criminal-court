#!/usr/bin/env python3
"""Parse the official Judicial Yuan court schedule CSV for Taiwan Qiaotou District Court.

The official site CSV observed in the user's sample has 10 columns and no header:
category, year, case_code, serial, date, time, courtroom, division, session_type, cause.

This first version deliberately accepts a downloaded CSV as input. Automated
retrieval from the official site's interactive form is a separate integration
step and must be verified before enabling unattended scheduled runs.
"""
from __future__ import annotations
import argparse
import csv
from collections import Counter
from pathlib import Path

HEADERS = ["案件類別", "年度", "字別", "案號流水號", "開庭日期", "開庭時間",
           "法庭", "股別", "庭類", "案由"]

def read_schedule(path: Path):
    rows = []
    # The sample official CSV is UTF-8/possibly BOM; try common Taiwan encodings.
    for enc in ("utf-8-sig", "cp950", "big5"):
        try:
            with path.open("r", encoding=enc, newline="") as f:
                rows = list(csv.reader(f))
            break
        except UnicodeDecodeError:
            continue
    if not rows:
        raise ValueError("無法解碼 CSV，請確認檔案編碼。")
    cleaned = []
    for line_no, row in enumerate(rows, 1):
        if not row or all(not str(x).strip() for x in row):
            continue
        if len(row) != 10:
            raise ValueError(f"第 {line_no} 列有 {len(row)} 欄，預期 10 欄；停止以免錯誤整理。")
        row = [str(x).strip() for x in row]
        if row[0] != "刑事":
            continue
        cleaned.append(dict(zip(HEADERS, row)))
    cleaned.sort(key=lambda r: (r["開庭日期"], r["開庭時間"], r["法庭"], r["年度"], r["字別"], r["案號流水號"]))
    return cleaned

def main():
    ap = argparse.ArgumentParser(description="整理橋頭地院官方刑事庭期 CSV")
    ap.add_argument("csv_file", type=Path, help="司法院庭期表下載的 CSV 檔")
    args = ap.parse_args()
    records = read_schedule(args.csv_file)
    print(f"刑事庭期筆數：{len(records)}")
    if not records:
        print("官方 CSV 中沒有刑事案件紀錄。")
        return
    print("\n" + " | ".join(HEADERS[4:9]))
    print("-" * 90)
    for r in records:
        time = r["開庭時間"]
        time = f"{time[:2]}:{time[2:]}" if len(time) == 4 and time.isdigit() else time
        case_no = f'{r["年度"]}.{r["字別"]}.{r["案號流水號"]}'
        print(f'{r["開庭日期"]} | {time} | {case_no} | {r["法庭"]} | {r["股別"]} | {r["庭類"]}')
    print("\n庭類統計：")
    for name, count in Counter(r["庭類"] for r in records).most_common():
        print(f"  {name}: {count}")

if __name__ == "__main__":
    main()
