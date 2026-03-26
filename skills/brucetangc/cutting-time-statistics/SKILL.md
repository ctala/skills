# Cutting Time Statistics Skill

## Prerequisites

**Requires Aiwei time template file to work!**

Template path: `/home/admin/.openclaw/media/inbound/艾威时间模板.xlsx`

Template file is not included, users need to prepare it themselves.

## Function

Extract cutting time from laser cutting PDF files, summarize by thickness, and generate Excel report in Aiwei template format.

## Usage

```bash
python3 calculator.py <zip_path> [output_path]
```

### Example

```bash
python3 calculator.py AW-25-2072.7z
# Output: AW-25-2072_Cutting_time_statistics.xlsx
```

## Features

- Extract thickness from PDF filename
- Extract cutting time from Job data in PDF
- Merge same thickness (e.g., 5mm + 5Mn)
- D column empty, E column with total time (2 decimal places)
- Auto-update formulas (F/H/L columns)
- Summary in remark row with border and center alignment
- Built-in self-check function

## Version

5.0.0
