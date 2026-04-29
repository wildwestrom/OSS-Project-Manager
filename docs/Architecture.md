# Architecture

The entire program lives in `main.py`. It is a single-file script with a handful of helper functions and a top-level driver under `if __name__ == "__main__"`.

## Module Layout

```
main.py
├── Helpers
│   ├── get_info()              → tuple of project metadata
│   ├── get_contributor_info()  → dict for one contributor
│   ├── track_issue()           → dict for one issue
│   └── ask_the_user()          → generic yes/no loop
├── Wrappers
│   ├── register_contributors() → list of contributor dicts
│   └── track_issues()          → list of issue dicts
└── Driver (__main__)
    ├── Section 1 — Launch
    ├── Section 2 — Track and Analyse Issues
    └── Section 3 — Save, Read and Report
```

## Functions

### `get_info() -> tuple[str, str, str, str, str]`

Prompts the user for project name, version, year started, language, and lead developer. The year is validated as an integer between 1940 and 2026; invalid input loops until a valid year is supplied. Returns the values as a tuple — chosen because project identity should be immutable for the rest of the run.

### `get_contributor_info() -> dict`

Reads name, language, and country from the user. Returns a dict with the additional defaults `role="new contributor"` and `commits=0`. The `status` field is added later in the driver.

### `track_issue() -> dict`

Generates an issue ID of the form `ISS-XXXX` from the first four characters of a UUID4. Validates `type`, `priority`, and `status` against the module-level sets `ISSUE_TYPES`, `PRIORITY_LEVELS`, and `STATUS_TYPES`. Returns a dict.

### `ask_the_user(yes_or_no_question, on_yes) -> list`

Generic helper that repeatedly prompts a yes/no question. On `yes`/`y`, it calls `on_yes()` and appends the result. On `no`/`n`, it returns the accumulated list. Anything else re-prompts.

### `register_contributors()` / `track_issues()`

Thin wrappers over `ask_the_user` that pair the prompt text with `get_contributor_info` or `track_issue`.

## Data Shapes

**Project info** — `tuple[str, str, int, str, str]` of `(name, version, year_started, language, lead_dev)`.

**Contributor** — `dict` with keys `name`, `role`, `language`, `commits`, `country`, `status`.

**Issue** — `dict` with keys `id`, `title`, `type`, `priority`, `reporter`, `status`. The `type` key is popped from the first issue mid-run as part of the dict-mutation demonstration.

## Constants

| Constant | Values |
|----------|--------|
| `ISSUE_TYPES` | `bug`, `feature` |
| `PRIORITY_LEVELS` | `critical`, `high`, `medium`, `low` |
| `STATUS_TYPES` | `open`, `in-progress`, `resolved` |

## Driver Flow

1. **Launch** — Collect project info, register contributors, sort contributor names, print a banner with tuple slicing, indexing, and `count`/`index` usage.
2. **Track and Analyse Issues** — Collect issues, count opens via a manual loop, mutate the first issue's priority to `critical`, build sets (`reporters`, `tech_stack`, `all_priorities`) and print their union/intersection/difference. Build `priority_count` and `status_groups` dicts via loops, then determine the top reporter without `max()` or `Counter`.
3. **Save, Read and Report** — Create an output folder named after the project (lowercased, spaces → underscores). Write `project_report.txt` and `issues.csv`. Read the report back three ways: `read()`, `readline()`, and `readlines()` (filtering for `critical`/`high` lines). Print a final summary, then append an "URGENT ISSUES" section in append mode and re-read the last six lines to confirm the append.

## Output Files

- **`<project>/project_report.txt`** — human-readable summary of project, contributors, issues, priority breakdown, top reporter, and (after the bonus step) a list of urgent issues.
- **`<project>/issues.csv`** — header `id,title,priority,reporter,status` followed by one row per issue.

## Error Handling

File operations are wrapped in `try`/`except` blocks for `IOError` (writes) and `FileNotFoundError` (reads). Input validation for the year and the bounded enums uses re-prompt loops rather than exceptions.
