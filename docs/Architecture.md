# Architecture

Single-file script: `main.py`. A few helper functions plus a top-level driver.

## Functions

| Function | Purpose |
|----------|---------|
| `get_info()` | Prompt for project name, version, year (1940–2026), language, lead. Returns a tuple. |
| `get_contributor_info()` | Prompt for name, language, country. Returns a dict. |
| `track_issue()` | Prompt for title, type, priority, status, reporter. Returns a dict with an `ISS-XXXX` id. |
| `ask_the_user(q, on_yes)` | Generic yes/no loop that calls `on_yes()` on each yes. |
| `register_contributors()` / `track_issues()` | Wrappers over `ask_the_user`. |

## Constants

- `ISSUE_TYPES` — `bug`, `feature`
- `PRIORITY_LEVELS` — `critical`, `high`, `medium`, `low`
- `STATUS_TYPES` — `open`, `in-progress`, `resolved`

## Driver Sections

1. **Launch** — collect project info and contributors, print banner.
2. **Track and Analyse Issues** — collect issues, build sets and dicts, find top reporter.
3. **Save, Read and Report** — write `project_report.txt` and `issues.csv` to a folder named after the project, read them back, append urgent issues.

## Output

- `<project>/project_report.txt` — summary report
- `<project>/issues.csv` — `id,title,priority,reporter,status`
