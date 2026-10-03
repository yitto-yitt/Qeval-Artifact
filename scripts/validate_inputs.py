from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_MANIFEST = ROOT / "data" / "retained_tasks.csv"
MODEL_NAMES = (
    "claude-opus-4-8",
    "deepseek-v4-pro",
    "deepseek-v4.1-flash",
    "gemini-3.5-flash",
    "gpt-5.3-codex-ssvip",
    "gpt-5.5",
    "gpt-6-astra",
    "grok-4.3",
    "qwen3-coder-480b-a35b-instruct",
    "qwen3.7-max-50off",
)
TRANSLATION_FRAMEWORKS = ("cirq", "pennylane", "qpanda", "qpanda2")
EXPECTED_PER_SLOT = 5
FILENAME = re.compile(r"^code(?P<task>\d+)_s(?P<sample>[1-5])\.py$")


def read_tasks() -> dict[int, int]:
    with TASK_MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    tasks: dict[int, int] = {}
    for row in rows:
        task_id = int(row["task_id"])
        class_id = int(row["class_id"])
        if task_id in tasks:
            raise ValueError(f"Duplicate task ID in manifest: {task_id}")
        if class_id not in (1, 2, 3):
            raise ValueError(f"Unexpected class ID for task {task_id}: {class_id}")
        tasks[task_id] = class_id
    expected = Counter({1: 20, 2: 9, 3: 49})
    actual = Counter(tasks.values())
    if len(tasks) != 78 or actual != expected:
        raise ValueError(f"Task manifest mismatch: total={len(tasks)}, classes={dict(actual)}")
    return tasks


def validate_candidate_dir(directory: Path, task_ids: set[int]) -> list[str]:
    errors: list[str] = []
    observed: dict[tuple[int, int], int] = Counter()
    for path in directory.glob("*.py"):
        match = FILENAME.fullmatch(path.name)
        if match is None:
            errors.append(f"Unexpected Python filename: {path.relative_to(ROOT)}")
            continue
        task_id = int(match.group("task"))
        sample_index = int(match.group("sample"))
        if task_id not in task_ids:
            errors.append(f"Task {task_id} is not retained: {path.relative_to(ROOT)}")
            continue
        observed[(task_id, sample_index)] += 1
    for task_id in sorted(task_ids):
        for sample_index in range(1, EXPECTED_PER_SLOT + 1):
            count = observed[(task_id, sample_index)]
            if count != 1:
                errors.append(
                    f"Expected one file for task={task_id}, sample={sample_index}; "
                    f"found {count} in {directory.relative_to(ROOT)}"
                )
    return errors


def check_setting(tasks: dict[int, int], branch: str) -> tuple[int, list[str]]:
    errors: list[str] = []
    total = 0
    for class_id in (1, 2, 3):
        task_ids = {task_id for task_id, task_class in tasks.items() if task_class == class_id}
        class_dir = ROOT / "data" / "candidates" / branch / f"class{class_id}"
        if not class_dir.is_dir():
            errors.append(f"Missing candidate class directory: {class_dir.relative_to(ROOT)}")
            continue
        present_models = {item.name for item in class_dir.iterdir() if item.is_dir()}
        if present_models != set(MODEL_NAMES):
            errors.append(
                f"Model directory mismatch in {class_dir.relative_to(ROOT)}: "
                f"missing={sorted(set(MODEL_NAMES)-present_models)}, "
                f"extra={sorted(present_models-set(MODEL_NAMES))}"
            )
        for model in MODEL_NAMES:
            model_dir = class_dir / model
            frameworks = ("qiskit",) if branch == "direct" else TRANSLATION_FRAMEWORKS
            for framework in frameworks:
                candidate_dir = model_dir / framework
                if not candidate_dir.is_dir():
                    errors.append(f"Missing candidate directory: {candidate_dir.relative_to(ROOT)}")
                    continue
                before = len(errors)
                errors.extend(validate_candidate_dir(candidate_dir, task_ids))
                if len(errors) == before:
                    count = sum(1 for _ in candidate_dir.glob("*.py"))
                    total += count
    return total, errors


def main() -> int:
    try:
        tasks = read_tasks()
        direct_count, direct_errors = check_setting(tasks, "direct")
        translation_count, translation_errors = check_setting(tasks, "translation")
    except (OSError, ValueError, KeyError) as error:
        print(f"Input validation failed: {error}", file=sys.stderr)
        return 1
    errors = direct_errors + translation_errors
    print(f"Retained tasks: {len(tasks)} (20 / 9 / 49)")
    print(f"Direct candidates: {direct_count} / 3,900")
    print(f"Translation candidates: {translation_count} / 15,600 across four frameworks")
    if errors:
        for error in errors[:100]:
            print(f"ERROR: {error}", file=sys.stderr)
        if len(errors) > 100:
            print(f"... and {len(errors)-100} additional errors", file=sys.stderr)
        return 1
    print("All expected task/model/framework/sample slots are present.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
