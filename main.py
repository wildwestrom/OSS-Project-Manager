import os
from typing import Callable
from uuid import uuid4
from semver import Version

def accept_alpha_only(prompt):
    while True:
        given_input = input(prompt)
        valid = True
        for ch in given_input:
            if not (ch.isalpha() or ch.isspace()):
                valid = False
        if len(given_input) == 0:
            valid = False
        if valid:
            break
        else:
            print("Input must be letters and spaces only")
    return given_input

def get_info() -> tuple[str, str, str, str, str]:
    name = input("Input name of project: ")
    version = None
    while version is None:
        maybe_version = input(f"What version is {name} at?: ")
        if not Version.is_valid(maybe_version):
            print(f"{maybe_version} is not a valid version number,")
            print("Adhere to semantic versioning conventions.")
            continue
        else:
            version = maybe_version
    year_started = None
    while year_started is None:
        maybe_year_started = input(f"What year was {name} started?: ")
        try:
            year_started = int(maybe_year_started)
        except ValueError:
            print("Year must be an integer")
            continue

        # I could've gotten the date at runtime but I was lazy
        if year_started < 1940 or year_started > 2026:
            print(f"There's no way {name} could've started in {year_started}.")
            year_started = None
            continue

    language = input("What is the main language of the project?: ")
    lead_dev = accept_alpha_only("What is the name of the leader of the project?: ")
    print()
    info = (name, version, year_started, language, lead_dev)
    return info

def get_contributor_info():
    name = accept_alpha_only("Input name: ")
    language = accept_alpha_only("Input language: ")
    ctry = accept_alpha_only("Input country: ")
    return {
        "name": name,
        "role": "new contributor",
        "language": language,
        "commits": 0,
        "country": ctry,
    }


ISSUE_TYPES = {"bug", "feature"}
PRIORITY_LEVELS = {"critical", "high", "medium", "low"}
STATUS_TYPES = {"open", "in-progress", "resolved"}


def track_issue():
    issue_id = f"ISS-{str(uuid4())[:4].upper()}"
    title = accept_alpha_only("Give a title to this issue: ")

    while True:
        issue_type = input("Is this a bug or a feature?: ").lower()
        if issue_type in ISSUE_TYPES:
            break
        else:
            print(f"Not one of {ISSUE_TYPES}")

    while True:
        priority = input("What priority is this?: ").lower()
        if priority in PRIORITY_LEVELS:
            break
        else:
            print(f"Not one of {PRIORITY_LEVELS}")

    while True:
        status = input("Is this issue open, in-progress, or resolved?: ").lower()
        if status in STATUS_TYPES:
            break
        else:
            print(f"Not one of {STATUS_TYPES}")

    name = accept_alpha_only(f"Who is reporting this {issue_type}?: ")

    return {
        "id": issue_id,
        "title": title,
        "type": issue_type,
        "priority": priority,
        "reporter": name,
        "status": status,
    }


def ask_yes_or_no(yes_or_no_question: str, on_yes: Callable):
    received_values = []
    while True:
        ans = input(yes_or_no_question).lower()
        match ans:
            case "yes" | "y":
                received_values.append(on_yes())
            case "no" | "n":
                break
            case _:
                print("\nWas that a yes or a no?")
                continue
    return received_values


def register_contributors():
    return ask_yes_or_no("Would you like to register a new contributor?: ", get_contributor_info)


def track_issues():
    return ask_yes_or_no("Would you like to add a new issue?: ", track_issue)


if __name__ == "__main__":
    # Section 1 — Launch Your Project

    print("=" * 40)
    print(" Welcum to projekt manager systum!")
    print("=" * 40)

    project_info = get_info()
    language = project_info[3]

    # Contributor registration
    contributors = register_contributors()
    print()

    names = []
    for contributor in contributors:
        contributor.update({"status": "Active"})
        names.append(contributor["name"])

    names.sort()

    # Show project info
    print("=" * 40)
    print(f"   {project_info[0]} — Open Source Project")
    print(f"   Project Lead: {project_info[4]}")
    print("=" * 40)
    print(f"Name: {project_info[0]} | Version {project_info[1]} | Started {project_info[2]}")
    print(f"First 3 fields: {project_info[:3]}")
    print(f"Language count: {project_info.count(language)}    Language index: {project_info.index(language)}")

    # project_info[0] = 'test'  → TypeError: 'tuple' object does not support item assignment
    # Tuples suit this data because project identity should be immutable after launch —
    # the name, version, and lead shouldn't change mid-run by accident.

    print("-" * 40)
    print(f"Sorted names: {names}")
    print(f"Last name: {names[-1]}     First two: {names[:2]}")

    first_contributor_backup = contributors[0].copy()
    print(f"Contributor 1 status: {contributors[0].get('status')}")
    print(f"Backup: {first_contributor_backup}")

    # Section 2 — Track and Analyse Issues

    issues = track_issues()

    # Count open issues without count()
    open_issues = 0
    for i in issues:
        if i["status"] == "open":
            open_issues += 1
    print(f"Open issues: {open_issues}")

    # Update first issue priority
    issues[0]["priority"] = "critical"
    print("First issue → priority updated to Critical.")

    # Last two issues via slice
    print(f"Last two issues: {issues[-2:]}")

    print("-" * 40)

    # Build reporters set and tech_stack set
    reporters = set()
    for i in issues:
        reporters.add(i["reporter"])

    tech_stack = set()
    for c in contributors:
        tech_stack.add(c["language"])

    tech_stack.add("TypeScript")
    tech_stack.discard("DreamBerd")  # discards safely even if not present

    all_priorities = set(i["priority"] for i in issues)

    print(f"reporters: {reporters}")
    print(f"tech_stack: {tech_stack}")
    print(f"union: {reporters.union(tech_stack)}")
    print(f"intersection: {reporters.intersection(tech_stack)}")
    print(f"difference: {reporters.difference(tech_stack)}")

    if "critical" in all_priorities:
        print("Critical present: YES — flag for immediate review.")
    else:
        print("Critical present: NO — nothing critical right now.")

    print("-" * 40)

    # Build priority_count by loop — no hardcoding
    priority_count = {}
    for i in issues:
        p = i["priority"]
        if p in priority_count:
            priority_count[p] += 1
        else:
            priority_count[p] = 1

    # Build status_groups — each key is a status, value is list of titles
    status_groups = {}
    for i in issues:
        s = i["status"]
        if s not in status_groups:
            status_groups[s] = []
        status_groups[s].append(i["title"])

    # Print using keys(), values(), items()
    print(f"priority keys: {priority_count.keys()}")
    print(f"priority values: {priority_count.values()}")

    status_line = " | ".join(
        f"{status.capitalize()}: {titles}" for status, titles in status_groups.items()
    )
    print(f"Status Groups → {status_line}")

    # Top reporter without max() or Counter()
    reporter_count = {}
    for i in issues:
        r = i["reporter"]
        if r in reporter_count:
            reporter_count[r] += 1
        else:
            reporter_count[r] = 1

    top_reporter = None
    top_count = 0
    for name, count in reporter_count.items():
        if count > top_count:
            top_reporter = name
            top_count = count

    print(f"Top reporter: {top_reporter} ({top_count} issues)")

    # pop 'type' from first issue
    issues[0].pop("type")
    print(f"After pop('type'): {issues[0]}")

    # Section 3 — Save, Read and Report

    project_name = project_info[0]
    folder_name = project_name.lower().replace(" ", "_")

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder created: {folder_name}/")
    else:
        print(f"Folder already exists: {folder_name}/")

    report_path = os.path.join(folder_name, "project_report.txt")
    csv_path = os.path.join(folder_name, "issues.csv")

    # Write project_report.txt
    try:
        with open(report_path, "w") as f:
            f.write("=" * 40 + "\n")
            f.write(f"{project_name} — PROJECT REPORT\n")
            f.write("=" * 40 + "\n\n")
            f.write(f"Project: {project_info[0]}\n")
            f.write(f"Version: {project_info[1]}\n")
            f.write(f"Started: {project_info[2]}\n")
            f.write(f"Language: {project_info[3]}\n")
            f.write(f"Lead: {project_info[4]}\n\n")
            f.write("--- CONTRIBUTORS ---\n")
            for c in contributors:
                f.write(f"  {c['name']} | {c['role']} | {c['language']} | {c['country']} | {c['status']}\n")
            f.write(f"\nSorted names: {names}\n")
            f.write(f"Tech stack: {tech_stack}\n\n")
            f.write("--- ISSUES ---\n")
            for i in issues:
                f.write(f"  [{i['id']}] {i['title']} | {i['priority']} | {i['reporter']} | {i['status']}\n")
            f.write(f"\nTotal issues: {len(issues)}\n")
            f.write(f"Open issues: {open_issues}\n")
            f.write(f"Reporters: {reporters}\n\n")
            f.write("--- PRIORITY BREAKDOWN ---\n")
            for p, cnt in priority_count.items():
                f.write(f"  {p}: {cnt}\n")
            f.write(f"\nTop reporter: {top_reporter} ({top_count} issues)\n")
    except IOError as e:
        print(f"Error writing report: {e}")

    # Write issues.csv
    try:
        with open(csv_path, "w") as f:
            f.write("id,title,priority,reporter,status\n")
            for i in issues:
                f.write(f"{i['id']},{i['title']},{i['priority']},{i['reporter']},{i['status']}\n")
    except IOError as e:
        print(f"Error writing CSV: {e}")

    print(f"Files saved: {os.listdir(folder_name)}")

    # Read back with read()
    try:
        with open(report_path, "r") as f:
            content = f.read()
        print("--- read() ---")
        print(content)
    except FileNotFoundError as e:
        print(f"Report not found: {e}")

    # Read back with readline()
    try:
        with open(report_path, "r") as f:
            print("--- readline() ---")
            print(f"Line 1: {f.readline()}", end="")
            print(f"Line 2: {f.readline()}", end="")
            print()
    except FileNotFoundError as e:
        print(f"Report not found: {e}")

    # Read back with readlines()
    try:
        with open(report_path, "r") as f:
            all_lines = f.readlines()
        critical_high_lines = [line for line in all_lines if "critical" in line.lower() or "high" in line.lower()]
        print("--- readlines() ---")
        print(f"Total lines: {len(all_lines)}    Critical/High lines: {len(critical_high_lines)}")
        for line in critical_high_lines:
            print(f"  {line}", end="")
        print()
    except FileNotFoundError as e:
        print(f"Report not found: {e}")

    # Finally done with all those damn try except blocks

    # Final summary — f-strings only, no hardcoding
    print("-" * 40)
    print("=" * 40)
    print(f"   {project_name} — FINAL SUMMARY")
    print("=" * 40)
    print(f"Project: {project_info[0]}    Version: {project_info[1]}    Lead: {project_info[4]}")
    print(f"Contributors: {len(contributors)}    Names: {names}")
    print(f"Tech Stack: {tech_stack}")
    print(f"Issues: {len(issues)}    Open: {open_issues}    Reporters: {len(reporters)}")
    print(f"Top Reporter: {top_reporter} ({top_count} issues)")
    priority_str = "  ".join(f"{p.capitalize()}:{c}" for p, c in priority_count.items())
    print(f"{priority_str}")
    print(f"Report: {report_path}")
    print(f"CSV: {csv_path}")
    print("=" * 40)
    print(f"{project_name} complete. Thank you for contributing to open source!")
    print("=" * 40)

    # Bonus — List comprehension + append mode

    urgent = [i["title"] for i in issues if i["priority"] in ("critical", "high")]
    print(f"\nUrgent issues: {urgent}")
    print(f"Urgent count: {len(urgent)}")

    try:
        with open(report_path, "a") as f:
            f.write("\n--- URGENT ISSUES ---\n")
            for title in urgent:
                f.write(f"  {title}\n")
    except IOError as e:
        print(f"Error appending to report: {e}")

    try:
        with open(report_path, "r") as f:
            last_lines = f.readlines()[-6:]
        print("\nLast 6 lines of report (confirming append):")
        for line in last_lines:
            print(f"  {line}", end="")
        print()
    except FileNotFoundError as e:
        print(f"Report not found: {e}")
