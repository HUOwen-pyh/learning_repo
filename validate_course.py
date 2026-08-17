"""检查六科课程结构、指定阅读材料和可运行练习。

默认只做静态检查；传入 --run 时逐个运行 Python 脚本。不会修改课程文件。
第六科后段使用 TypeScript；当前环境没有 Node 时仍做结构静态检查。
"""
from __future__ import annotations

import argparse
import ast
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
COURSES = {
    "01_高级数据结构与算法": {"count": 30, "width": 2},
    "02_组合优化": {"count": 30, "width": 2},
    "03_近似算法": {"count": 30, "width": 2},
    "04_计算理论": {"count": 30, "width": 2},
    "05_SAT算法": {"count": 30, "width": 2},
    "06_程序语言理论_范畴语义与LLM工程": {"count": 196, "width": 3},
}
REQUIRED_READ_MARKERS = ("目标", "分钟", "验收")
ADVANCED_SUBJECT = "06_程序语言理论_范畴语义与LLM工程"
HARNESS_SHA = "47f943859bef60e4160492346772ded9b24f765a"


def matching_section(text: str, title_pattern: str) -> str:
    """Return the first level-two section whose title matches a semantic family."""
    headings = list(re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE))
    for index, heading in enumerate(headings):
        if not re.search(title_pattern, heading.group(1), re.IGNORECASE):
            continue
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[start:end]
    return ""


def table_minutes(section_text: str) -> list[int]:
    """Accept either a duration column (`18`) or a time range (`5–15`)."""
    minutes: list[int] = []
    for line in section_text.splitlines():
        range_match = re.match(r"^\|\s*(\d+)\s*[–-]\s*(\d+)\s*\|", line)
        if range_match:
            left, right = map(int, range_match.groups())
            if 0 <= left < right <= 60:
                minutes.append(right - left)
            continue
        duration_match = re.match(r"^\|\s*(\d+)\s*\|", line)
        if duration_match:
            value = int(duration_match.group(1))
            if 0 < value <= 40:
                minutes.append(value)
    return minutes


def check_advanced_read(read_file: Path, text: str, errors: list[str]) -> None:
    relative = read_file.relative_to(ROOT)
    section_families = {
        "goal": r"目标",
        "prerequisite": r"前置",
        "required reading": r"必读",
        "reading guide": r"导读|导引",
        "derivation or proof": r"推导|证明",
        "Harness/LLM connection": r"Harness|LLM|工业联系",
        "60-minute schedule": r"^(?:严格\s*)?60\s*分钟(?:安排)?$",
        "acceptance": r"验收",
        "optional extension": r"可选延伸",
    }
    found_sections = {
        label: matching_section(text, pattern)
        for label, pattern in section_families.items()
    }
    for label, content in found_sections.items():
        if not content:
            errors.append(f"{relative}: missing {label} section")
    required = found_sections["required reading"]
    if "https://" not in required:
        errors.append(f"{relative}: required reading has no authoritative URL")
    range_markers = (
        "精确", "§", "页", "章", "Chapter", "Lecture", "Definition", "Theorem",
        "定义", "定理", "从", "至", "行", "标题", "小节", "#L",
    )
    if required and not any(marker in required for marker in range_markers):
        errors.append(f"{relative}: required reading has no precise range")
    reading_minutes = table_minutes(required)
    if not reading_minutes or not 15 <= sum(reading_minutes) <= 40:
        errors.append(f"{relative}: required reading minutes are {reading_minutes}, expected total 15..40")
    if "github.com/deepseek-ai/deepseek-harness" in required and HARNESS_SHA not in required:
        errors.append(f"{relative}: Harness required reading is not pinned to {HARNESS_SHA[:8]}")
    schedule = found_sections["60-minute schedule"]
    intervals: list[tuple[int, int]] = []
    for line in schedule.splitlines():
        # In tables, only the first cell is a time slot; prose in later cells may
        # legitimately contain ranges such as "写 2–3 句".
        candidates = (
            re.findall(r"^\|\s*(\d+)\s*[–—-]\s*(\d+)\s*\|", line)
            if line.lstrip().startswith("|")
            else re.findall(r"(?<!\d)(\d+)\s*[–—-]\s*(\d+)(?!\d)", line)
        )
        intervals.extend(
            (int(a), int(b)) for a, b in candidates
            if 0 <= int(a) < int(b) <= 60
        )
    if intervals:
        if intervals[0][0] != 0 or intervals[-1][1] != 60:
            errors.append(f"{relative}: schedule does not span 0..60: {intervals}")
        elif any(right != next_left for (_, right), (next_left, _) in zip(intervals, intervals[1:])):
            errors.append(f"{relative}: schedule has a gap or overlap: {intervals}")
    else:
        durations = []
        for line in schedule.splitlines():
            if "合计" in line:
                continue
            match = re.match(r"^\|[^|]+\|\s*\*{0,2}(\d+)\*{0,2}\s*\|", line)
            if match:
                durations.append(int(match.group(1)))
        if not durations or sum(durations) != 60:
            errors.append(f"{relative}: schedule durations do not total 60: {durations}")
    if re.search(r"(?im)^\s*(?:TBD|TODO|待补(?:充)?|占位(?:内容)?)\s*$", text):
        errors.append(f"{relative}: contains placeholder text")


def static_checks(subject_filter: str | None = None) -> tuple[list[Path], list[Path], list[str], int]:
    python_practices: list[Path] = []
    typescript_practices: list[Path] = []
    errors: list[str] = []
    task_total = 0
    selected = {
        name: spec for name, spec in COURSES.items()
        if subject_filter is None or name.startswith(subject_filter)
    }
    if not selected:
        return python_practices, typescript_practices, [f"unknown subject filter: {subject_filter}"], task_total
    for subject_name, spec in selected.items():
        subject = ROOT / subject_name
        if not (subject / "README.md").is_file():
            errors.append(f"{subject_name}: missing README.md")
        tasks_root = subject / "tasks"
        if subject.is_dir():
            subject_entries = {entry.name for entry in subject.iterdir()}
            expected_subject_entries = {"README.md", "tasks"}
            if subject_entries != expected_subject_entries:
                errors.append(
                    f"{subject_name}: entries are {sorted(subject_entries)}, "
                    f"expected {sorted(expected_subject_entries)}"
                )
        width = int(spec["width"])
        if tasks_root.is_dir():
            unexpected_task_root_entries = [
                entry.name for entry in tasks_root.iterdir()
                if not entry.is_dir() or not re.fullmatch(rf"\d{{{width}}}_.+", entry.name)
            ]
            if unexpected_task_root_entries:
                errors.append(
                    f"{subject_name}/tasks: unexpected entries "
                    f"{sorted(unexpected_task_root_entries)}"
                )
        task_dirs = sorted((p for p in tasks_root.iterdir()
                            if p.is_dir() and re.fullmatch(rf"\d{{{width}}}_.+", p.name)),
                           key=lambda p: p.name) if tasks_root.is_dir() else []
        expected_count = int(spec["count"])
        task_total += len(task_dirs)
        if len(task_dirs) != expected_count:
            errors.append(f"{subject_name}: expected {expected_count} task directories, found {len(task_dirs)}")
        prefixes = [p.name[:width] for p in task_dirs]
        expected = [f"{i:0{width}}" for i in range(1, expected_count + 1)]
        if prefixes != expected:
            errors.append(f"{subject_name}: task prefixes are not exactly {expected[0]}..{expected[-1]}")
        for task in task_dirs:
            read_file = task / "read.md"
            task_number = int(task.name[:width])
            practice_name = "practice.ts" if subject_name == ADVANCED_SUBJECT and task_number >= 162 else "practice.py"
            practice = task / practice_name
            actual_entries = {p.name for p in task.iterdir()}
            expected_entries = {"read.md", practice_name}
            if actual_entries != expected_entries:
                errors.append(
                    f"{task.relative_to(ROOT)}: entries are {sorted(actual_entries)}, "
                    f"expected {sorted(expected_entries)}"
                )
            if read_file.is_file():
                text = read_file.read_text(encoding="utf-8")
                for marker in REQUIRED_READ_MARKERS:
                    if marker not in text:
                        errors.append(f"{read_file.relative_to(ROOT)}: missing marker {marker!r}")
                if len(text) < 500:
                    errors.append(f"{read_file.relative_to(ROOT)}: reading is too short ({len(text)} chars)")
                if subject_name == ADVANCED_SUBJECT:
                    check_advanced_read(read_file, text, errors)
            if practice.is_file():
                source = practice.read_text(encoding="utf-8")
                if practice.suffix == ".py":
                    python_practices.append(practice)
                    try:
                        ast.parse(source, filename=str(practice))
                    except SyntaxError as exc:
                        errors.append(f"{practice.relative_to(ROOT)}: {exc}")
                else:
                    typescript_practices.append(practice)
                    non_erasable = (
                        r"(?m)^\s*(?:const\s+)?enum\s+",
                        r"(?m)^\s*namespace\s+",
                        r"constructor\s*\([^)]*\b(?:public|private|protected|readonly)\b",
                        r"(?m)^\s*@\w+",
                        r"(?m)^\s*import\s+\w+\s*=",
                    )
                    if any(re.search(pattern, source) for pattern in non_erasable):
                        errors.append(
                            f"{practice.relative_to(ROOT)}: uses non-erasable TypeScript syntax; "
                            "standalone exercises must run with Node type stripping"
                        )
                if not re.search(r"\bassert\b", source):
                    errors.append(f"{practice.relative_to(ROOT)}: no executable assertion")
                if subject_name == ADVANCED_SUBJECT and not re.search(
                    r"动手改造|hands-on|改造|\bedit\b|修改|扩展", source, re.IGNORECASE
                ):
                    errors.append(f"{practice.relative_to(ROOT)}: missing hands-on modification")
    return python_practices, typescript_practices, errors, task_total


def run_practices(
    practices: list[Path], timeout: float, command_prefix: list[str], label: str
) -> list[str]:
    errors: list[str] = []
    for index, practice in enumerate(practices, 1):
        relative = practice.relative_to(ROOT)
        try:
            completed = subprocess.run(
                [*command_prefix, str(practice)],
                cwd=practice.parent,
                text=True,
                encoding="utf-8",
                errors="replace",
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                capture_output=True,
                timeout=timeout,
                check=False,
            )
        except subprocess.TimeoutExpired:
            errors.append(f"{relative}: TIMEOUT after {timeout:g}s")
            continue
        if completed.returncode:
            tail = (completed.stdout + completed.stderr).strip().splitlines()[-8:]
            errors.append(f"{relative}: exit {completed.returncode}\n    " + "\n    ".join(tail))
        else:
            print(f"[{label} {index:03}/{len(practices):03}] PASS {relative.parent}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true", help="execute every practice.py")
    parser.add_argument("--timeout", type=float, default=20.0, help="seconds per script")
    parser.add_argument("--subject", help="course prefix such as 06; default checks all")
    args = parser.parse_args()
    python_practices, typescript_practices, errors, task_total = static_checks(args.subject)
    if args.run and not errors:
        errors.extend(run_practices(
            python_practices, args.timeout, [sys.executable, "-B"], "PY"
        ))
        node = shutil.which("node")
        if typescript_practices and node:
            errors.extend(run_practices(
                typescript_practices, args.timeout, [node], "TS"
            ))
        elif typescript_practices:
            print(
                f"[TS SKIP] Node not found; {len(typescript_practices)} TypeScript practices "
                "received static/erasable-syntax checks only"
            )
    subject_count = len(COURSES) if args.subject is None else sum(name.startswith(args.subject) for name in COURSES)
    print(
        f"subjects={subject_count} tasks={task_total} "
        f"python_practices={len(python_practices)} "
        f"typescript_practices={len(typescript_practices)} errors={len(errors)}"
    )
    for error in errors:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
