# Usage

Once you run the program, it walks you through three sections.

## Section 1 — Project Setup

You will be prompted for:

- **Project name**
- **Version** (e.g. `1.0.0`)
- **Year started** — must be a valid integer between 1940 and 2026
- **Main language**
- **Project lead name**

Then you can register contributors. For each contributor you provide a name, language, and country. Enter `no` (or `n`) when done.

## Section 2 — Issue Tracking

Add issues one at a time. Each issue requires:

| Field | Options |
|-------|---------|
| Title | any text |
| Type | `bug` or `feature` |
| Priority | `critical`, `high`, `medium`, `low` |
| Status | `open`, `in-progress`, `resolved` |
| Reporter | any name |

Each issue gets an auto-generated ID like `ISS-A3F1`. Enter `no` when done adding issues.

After entry the program prints a summary: open issue count, top reporter, priority breakdown, and status groups.

## Section 3 — Output Files

Two files are saved to a folder named after your project (spaces replaced with underscores):

- `project_report.txt` — full project summary including contributors, issues, and priority breakdown
- `issues.csv` — issue list with columns: `id, title, priority, reporter, status`

The report is also printed to the terminal at the end of the run.
