import argparse
import ast
import csv
import importlib.util
import importlib.metadata
import json
import math
import platform
import re
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape
SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE_DIR = SCRIPT_DIR.parent
DEFAULT_REPORTS_DIR = SCRIPT_DIR / 'reports'
DEFAULT_QISKIT_PYTHON = WORKSPACE_DIR / '.venv-qpanda-align' / 'Scripts' / 'python.exe'
DEFAULT_QPANDA2_PYTHON = WORKSPACE_DIR / '.venv-qpanda384' / 'Scripts' / 'python.exe'
JSD_THRESHOLD = 0.02
TVD_THRESHOLD = 0.05
FIDELITY_THRESHOLD = 0.95
FRAMEWORK_NAMES = {'cirq': 'Cirq', 'qpanda': 'pyQPanda3', 'qpanda2': 'pyQPanda'}
NO_ARG_TASKS = {1, 14, 15, 28, 31, 61, 92}
BV_CASES = {'all_zero': ('0',), 'nontrivial': ('110',)}
SUPERDENSE_CASES = {'bits_00': ('00',), 'bits_01': ('01',), 'bits_10': ('10',), 'bits_11': ('11',)}
SIMON_CASES = {'zero_secret': ('00',), 'nontrivial_secret': ('110',)}
CHSH_CASES = {'alice0_bob0': (0, 0), 'alice0_bob1': (0, 1), 'alice1_bob0': (1, 0), 'alice1_bob1': (1, 1)}
PROBABILITY_DIST_CASES = {'deterministic': ({0: 1.0},), 'nonuniform': ({0: 0.25, 1: 0.25, 2: 0.5},)}
LOGIC_TWO_ARG_CASES = {'a0_b0': (0, 0), 'a0_b7': (0, 7), 'a3_b5': (3, 5), 'a7_b7': (7, 7)}
NOT_CASES = {'a0': (0,), 'a1': (1,), 'a3': (3,), 'a7': (7,)}

@dataclass(frozen=True)
class Task:
    task_id: int
    function_name: str

def read_text_auto(path: Path) -> str:
    for encoding in ('utf-8-sig', 'utf-8', 'gb18030'):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding='utf-8', errors='replace')

def parse_task_filter(raw: str | None) -> set[int] | None:
    if raw is None or raw.strip().lower() == 'all':
        return None
    task_ids: set[int] = set()
    for part in raw.split(','):
        item = part.strip()
        if not item:
            continue
        task_ids.add(int(item))
    return task_ids

def parse_frameworks(raw: str) -> list[str]:
    frameworks = [item.strip().lower() for item in raw.split(',') if item.strip()]
    if not frameworks:
        raise ValueError('At least one framework is required.')
    unknown = [item for item in frameworks if item not in FRAMEWORK_NAMES]
    if unknown:
        raise ValueError(f'Unknown framework(s): {', '.join(unknown)}')
    return frameworks

def parse_tasks_from_std(std_dir: Path, raw_filter: str | None=None) -> list[Task]:
    if not std_dir.is_dir():
        raise NotADirectoryError(f'Expected a directory of Qiskit standard code files, got: {std_dir}')
    wanted = parse_task_filter(raw_filter)
    tasks: list[Task] = []
    code_paths = sorted(std_dir.glob('code*.py'), key=lambda path: int(re.search('\\d+', path.stem).group(0)))
    for code_path in code_paths:
        match = re.fullmatch('code(\\d+)', code_path.stem)
        if match is None:
            continue
        task_id = int(match.group(1))
        if wanted is not None and task_id not in wanted:
            continue
        qiskit_code = read_text_auto(code_path).strip() + '\n'
        function_name = first_public_function_name(qiskit_code)
        tasks.append(Task(task_id=task_id, function_name=function_name))
    if wanted is not None:
        found = {task.task_id for task in tasks}
        missing = wanted.difference(found)
        if missing:
            raise ValueError('Task id(s) not found in std dir: ' + ', '.join((str(item) for item in sorted(missing))))
    return tasks

def first_public_function_name(code: str) -> str:
    tree = ast.parse(code)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and (not node.name.startswith('_')):
            return node.name
    raise ValueError('No public function found in code block.')

def safe_dir_name(name: str) -> str:
    return re.sub('[^A-Za-z0-9._-]+', '_', name).strip('._') or 'model'

def sample_suffix(sample_index: int) -> str:
    if sample_index < 1:
        raise ValueError(f'Sample index must be positive, got {sample_index}')
    return f'_s{sample_index}'

def candidate_file_name(task_id: int, sample_index: int) -> str:
    return f'code{task_id}{sample_suffix(sample_index)}.py'

def candidate_path_for_sample(output_dir: Path, model: str, framework: str, task_id: int, sample_index: int) -> Path:
    return output_dir / model / framework / candidate_file_name(task_id, sample_index)

def discover_candidate_samples(output_dir: Path, model: str, framework: str, task_id: int) -> list[tuple[int, Path]]:
    framework_dir = output_dir / model / framework
    if not framework_dir.is_dir():
        return []
    candidates: list[tuple[int, Path]] = []
    base_path = framework_dir / candidate_file_name(task_id, 1)
    if base_path.is_file():
        candidates.append((1, base_path))
    suffix_pattern = re.compile(f'^code{task_id}_s(\\d+)\\.py$')
    for path in sorted(framework_dir.glob(f'code{task_id}_s*.py')):
        match = suffix_pattern.match(path.name)
        if match is None:
            continue
        sample_index = int(match.group(1))
        if sample_index <= 1:
            continue
        candidates.append((sample_index, path))
    candidates.sort(key=lambda item: item[0])
    return candidates

def case_labels_for_task(task_id: int) -> list[str]:
    if task_id in NO_ARG_TASKS:
        return ['default']
    if task_id == 24:
        return ['constant_oracle', 'balanced_oracle']
    if task_id == 37:
        return list(BV_CASES)
    if task_id == 40:
        return ['fixed_normalized_vector']
    if task_id == 47:
        return ['samples_1024']
    if task_id == 52:
        return list(SUPERDENSE_CASES)
    if task_id in {53, 54, 55}:
        return list(LOGIC_TWO_ARG_CASES)
    if task_id == 56:
        return list(NOT_CASES)
    if task_id == 64:
        return list(SIMON_CASES)
    if task_id == 67:
        return list(CHSH_CASES)
    if task_id == 68:
        return ['bomb_live_false', 'bomb_live_true']
    if task_id == 77:
        return list(PROBABILITY_DIST_CASES)
    raise ValueError(f'No case registry for task {task_id}')

def default_repeats_for_task(task_id: int, base_repeats: int, low_shot_repeats: int) -> int:
    if task_id == 14:
        return low_shot_repeats
    if task_id == 37:
        return 128
    return base_repeats

def resolve_models_for_evaluation(raw_models: str, output_dir: Path) -> list[str]:
    if raw_models.strip().lower() == 'all':
        if not output_dir.exists():
            return []
        return sorted((path.name for path in output_dir.iterdir() if path.is_dir()))
    return [safe_dir_name(item.strip()) for item in raw_models.split(',') if item.strip()]

def evaluate(args: argparse.Namespace) -> int:
    std_dir = Path(args.std_dir)
    tasks = parse_tasks_from_std(std_dir, args.tasks)
    if args.limit is not None:
        tasks = tasks[:args.limit]
    frameworks = parse_frameworks(args.frameworks)
    output_dir = Path(args.output_dir)
    standard_python = resolve_python_executable(getattr(args, 'qiskit_python', None), DEFAULT_QISKIT_PYTHON, 'Qiskit standard-answer')
    framework_pythons = {'qpanda2': resolve_python_executable(getattr(args, 'qpanda2_python', None), DEFAULT_QPANDA2_PYTHON, 'qpanda2 candidate')}
    models = resolve_models_for_evaluation(args.models, output_dir)
    reports_dir = resolve_reports_dir(args.reports_dir, models)
    reports_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    standard_cache: dict[tuple[int, str, int], dict[str, Any]] = {}
    candidate_cache: dict[tuple[str, str, int], dict[str, Any]] = {}
    print(f'Std dir: {std_dir}')
    print(f'Outputs dir: {output_dir}')
    print(f'Reports dir: {reports_dir}')
    print(f'Models: {(', '.join(models) if models else '(none found)')}')
    print(f'Frameworks: {', '.join(frameworks)}')
    print(f'Qiskit standard Python: {standard_python}')
    if 'qpanda2' in frameworks:
        print(f'qpanda2 candidate Python: {framework_pythons['qpanda2']}')
    for model in models:
        for framework in frameworks:
            for task in tasks:
                task_id = task.task_id
                standard_path = std_dir / f'code{task_id}.py'
                labels = case_labels_for_task(task_id)
                repeats = default_repeats_for_task(task_id, args.repeats, args.low_shot_repeats)
                sample_paths = discover_candidate_samples(output_dir, model, framework, task_id)
                if not sample_paths:
                    sample_paths = [(1, candidate_path_for_sample(output_dir, model, framework, task_id, 1))]
                for sample_index, candidate_path in sample_paths:
                    for case_label in labels:
                        base_row = {'model': model, 'framework': framework, 'task_id': task_id, 'function': task.function_name, 'sample_index': sample_index, 'case': case_label, 'repeats': repeats, 'candidate_path': str(candidate_path)}
                        if not candidate_path.is_file():
                            rows.append({**base_row, 'status': 'FAIL', 'judgeable': False, 'alignment': '', 'jsd': '', 'tvd': '', 'classical_fidelity': '', 'error': f'Missing candidate file: {candidate_path}'})
                            continue
                        standard_cache_key = (task_id, case_label, repeats)
                        if standard_cache_key not in standard_cache:
                            standard_cache[standard_cache_key] = run_case_subprocess(module_path=standard_path, function_name=task.function_name, task_id=task_id, framework='qiskit', case_label=case_label, repeats=repeats, timeout=args.case_timeout, python_exe=standard_python)
                        standard_result = standard_cache[standard_cache_key]
                        candidate_cache_key = (str(candidate_path), case_label, repeats)
                        if candidate_cache_key not in candidate_cache:
                            candidate_cache[candidate_cache_key] = run_case_subprocess(module_path=candidate_path, function_name=task.function_name, task_id=task_id, framework=framework, case_label=case_label, repeats=repeats, timeout=args.case_timeout, python_exe=framework_pythons.get(framework, Path(sys.executable)))
                        candidate_result = candidate_cache[candidate_cache_key]
                        if not standard_result.get('ok'):
                            rows.append({**base_row, 'status': 'FAIL', 'judgeable': False, 'alignment': '', 'jsd': '', 'tvd': '', 'classical_fidelity': '', 'error': 'standard failed: ' + str(standard_result.get('error', ''))})
                            continue
                        if not candidate_result.get('ok'):
                            rows.append({**base_row, 'status': 'FAIL', 'judgeable': False, 'alignment': '', 'jsd': '', 'tvd': '', 'classical_fidelity': '', 'error': str(candidate_result.get('error', ''))})
                            continue
                        standard_dist = standard_result['distribution']
                        candidate_dist = candidate_result['distribution']
                        alignment, metrics = pick_best_alignment(standard_dist, candidate_dist)
                        passed = metrics['jsd'] <= JSD_THRESHOLD and metrics['tvd'] <= TVD_THRESHOLD and (metrics['classical_fidelity'] >= FIDELITY_THRESHOLD)
                        rows.append({**base_row, 'status': 'PASS' if passed else 'FAIL', 'judgeable': True, 'alignment': alignment, 'jsd': metrics['jsd'], 'tvd': metrics['tvd'], 'classical_fidelity': metrics['classical_fidelity'], 'error': ''})
                        print('[{status}] {model} {framework} code{task_id} sample {sample_index} {case} JSD={jsd:.5g} TVD={tvd:.5g} F={fid:.5g} align={align}'.format(status='PASS' if passed else 'FAIL', model=model, framework=framework, task_id=task_id, sample_index=sample_index, case=case_label, jsd=metrics['jsd'], tvd=metrics['tvd'], fid=metrics['classical_fidelity'], align=alignment), flush=True)
    write_reports(rows, reports_dir, tasks, models, frameworks, std_dir, output_dir)
    print(f'Wrote raw-style reports under {reports_dir / '<model>' / '<framework>'}')
    return 0

def run_case_subprocess(*, module_path: Path, function_name: str, task_id: int, framework: str, case_label: str, repeats: int, timeout: float, python_exe: Path) -> dict[str, Any]:
    cmd = [str(python_exe), str(Path(__file__).resolve()), '_run_case', '--module', str(module_path), '--function-name', function_name, '--task-id', str(task_id), '--framework', framework, '--case', case_label, '--repeats', str(repeats)]
    try:
        proc = subprocess.run(cmd, cwd=str(WORKSPACE_DIR), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired:
        return {'ok': False, 'error': f'Timed out after {timeout} seconds'}
    if proc.returncode != 0:
        return {'ok': False, 'error': (proc.stderr or proc.stdout or f'exit code {proc.returncode}').strip()}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {'ok': False, 'error': 'Subprocess returned non-JSON stdout: ' + proc.stdout[:2000]}

def resolve_python_executable(configured_path: str | Path | None, default_path: Path, label: str) -> Path:
    python_path = Path(configured_path) if configured_path else default_path
    python_path = python_path.expanduser()
    if not python_path.is_file():
        raise FileNotFoundError(f'{label} Python not found: {python_path}')
    return python_path

def write_reports(rows: list[dict[str, Any]], reports_dir: Path, tasks: list[Task], models: list[str], frameworks: list[str], std_dir: Path, output_dir: Path) -> None:
    fieldnames = ['model', 'framework', 'task_id', 'function', 'sample_index', 'case', 'repeats', 'status', 'judgeable', 'alignment', 'jsd', 'tvd', 'classical_fidelity', 'error', 'candidate_path']
    write_framework_flat_results(rows, reports_dir, models, frameworks, fieldnames)
    write_raw_style_reports(rows, reports_dir, tasks, models, frameworks, std_dir, output_dir)

def write_flat_results(rows: list[dict[str, Any]], report_dir: Path, fieldnames: list[str]) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    csv_path = report_dir / 'results.csv'
    jsonl_path = report_dir / 'results.jsonl'
    with csv_path.open('w', encoding='utf-8-sig', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({name: row.get(name, '') for name in fieldnames})
    with jsonl_path.open('w', encoding='utf-8') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')

def write_framework_flat_results(rows: list[dict[str, Any]], reports_dir: Path, models: list[str], frameworks: list[str], fieldnames: list[str]) -> None:
    for model in models:
        for framework in frameworks:
            subset = [row for row in rows if row.get('model') == model and row.get('framework') == framework]
            write_flat_results(subset, reports_dir / model / framework, fieldnames)

def write_raw_style_reports(rows: list[dict[str, Any]], reports_dir: Path, tasks: list[Task], models: list[str], frameworks: list[str], std_dir: Path, output_dir: Path) -> None:
    for model in models:
        for framework in frameworks:
            subset = [row for row in rows if row.get('model') == model and row.get('framework') == framework]
            target_dir = reports_dir / model / framework
            details = build_raw_style_details(subset, tasks, model, framework, std_dir, output_dir)
            classification = build_classification_rows(details)
            summary = build_summary(classification)
            fail_samples = build_fail_samples(classification, details)
            error_samples = build_error_samples(classification, details)
            details['summary'] = summary
            target_dir.mkdir(parents=True, exist_ok=True)
            write_json(target_dir / 'raw_details.json', details)
            write_text(target_dir / 'raw_report.txt', build_raw_text_report(details))
            write_text(target_dir / 'environment.txt', build_environment_text(details['environment']))
            write_jsonl(target_dir / 'classification.jsonl', classification)
            write_summary_csv(target_dir / 'summary.csv', summary)
            write_json(target_dir / 'fail_samples.json', fail_samples)
            write_json(target_dir / 'error_samples.json', error_samples)
            write_metrics_xlsx(target_dir / 'metrics.xlsx', details)

def build_raw_style_details(rows: list[dict[str, Any]], tasks: list[Task], model: str, framework: str, std_dir: Path, output_dir: Path) -> dict[str, Any]:
    rows_by_task: dict[int, dict[int, list[dict[str, Any]]]] = {}
    for row in rows:
        task_id = int(row['task_id'])
        sample_index = to_int_or_none(row.get('sample_index')) or 1
        rows_by_task.setdefault(task_id, {}).setdefault(sample_index, []).append(row)
    results = []
    for task in tasks:
        task_samples = rows_by_task.get(task.task_id, {})
        samples: list[dict[str, Any]] = []
        for sample_index in sorted(task_samples):
            sample_rows = sorted(task_samples[sample_index], key=lambda row: str(row.get('case', '')))
            candidate_path = sample_rows[0].get('candidate_path') or candidate_path_for_sample(output_dir, model, framework, task.task_id, sample_index)
            cases = [build_raw_case(row) for row in sample_rows]
            sample_pass = bool(cases) and all((case['status'] == 'PASS' for case in cases))
            sample_status = aggregate_case_status(cases)
            samples.append({'sample_index': sample_index, 'candidate_path': str(candidate_path), 'cases': cases, 'sample_count': len(cases), 'sample_pass': sample_pass, 'sample_status': sample_status, 'sample_label': 'PASS' if sample_pass else 'FAIL'})
        pass_count, pass_at_1, pass_at_3, pass_at_5 = task_pass_metrics(samples)
        best_sample = next((sample for sample in samples if sample['sample_pass']), None)
        primary_sample = samples[0] if samples else None
        setup_error = None if samples else 'No evaluation rows were produced for this task.'
        results.append({'task_id': task.task_id, 'class_id': 1, 'path_a': str(std_dir / f'code{task.task_id}.py'), 'path_b': str(primary_sample['candidate_path']) if primary_sample else str(candidate_path_for_sample(output_dir, model, framework, task.task_id, 1)), 'function': task.function_name, 'framework': framework, 'model': model, 'samples': samples, 'sample_count': len(samples), 'pass_count': pass_count, 'pass_at_1': pass_at_1, 'pass_at_3': pass_at_3, 'pass_at_5': pass_at_5, 'best_sample_index': None if best_sample is None else best_sample['sample_index'], 'best_sample_path': None if best_sample is None else best_sample['candidate_path'], 'raw_status': aggregate_task_status(samples), 'raw_label': 'PASS' if pass_count > 0 else 'FAIL', 'setup_error': setup_error})
    return {'mode': 'cross_language_raw_style', 'dir_a': str(std_dir), 'dir_b': str(output_dir / model / framework), 'model': model, 'framework': framework, 'thresholds': {'jsd_max': JSD_THRESHOLD, 'tvd_max': TVD_THRESHOLD, 'classical_fidelity_min': FIDELITY_THRESHOLD}, 'environment': build_environment(framework), 'summary': {}, 'results': results}

def task_pass_metrics(samples: list[dict[str, Any]]) -> tuple[int, float | None, float | None, float | None]:
    sample_passes = [bool(sample.get('sample_pass')) for sample in samples]
    pass_count = sum((1 for passed in sample_passes if passed))
    if any((sample.get('sample_status', infer_sample_status(sample)) == 'ERROR' for sample in samples)):
        return (pass_count, None, None, None)
    return (pass_count, estimate_pass_at_k(len(sample_passes), pass_count, 1), estimate_pass_at_k(len(sample_passes), pass_count, 3), estimate_pass_at_k(len(sample_passes), pass_count, 5))

def aggregate_case_status(cases: list[dict[str, Any]]) -> str:
    statuses = [str(case.get('status', 'FAIL')) for case in cases]
    return 'PASS' if statuses and all((status == 'PASS' for status in statuses)) else 'FAIL'

def infer_sample_status(sample: dict[str, Any]) -> str:
    if sample.get('setup_error'):
        return 'FAIL'
    return aggregate_case_status(sample.get('cases', []) or [])

def aggregate_task_status(samples: list[dict[str, Any]]) -> str:
    statuses = [sample.get('sample_status', infer_sample_status(sample)) for sample in samples]
    return 'PASS' if 'PASS' in statuses else 'FAIL'

def estimate_pass_at_k(sample_count: int, pass_count: int, k: int) -> float | None:
    if sample_count <= 0 or k <= 0 or sample_count < k:
        return None
    if pass_count <= 0:
        return 0.0
    if sample_count - pass_count < k:
        return 1.0
    return 1.0 - math.comb(sample_count - pass_count, k) / math.comb(sample_count, k)

def build_raw_case(row: dict[str, Any]) -> dict[str, Any]:
    status = 'PASS' if row.get('status') == 'PASS' else 'FAIL'
    return {'label': row.get('case'), 'sample_index': to_int_or_none(row.get('sample_index')), 'repeat': to_int_or_none(row.get('repeats')), 'jsd': to_float_or_none(row.get('jsd')), 'tvd': to_float_or_none(row.get('tvd')), 'classical_fidelity': to_float_or_none(row.get('classical_fidelity')), 'status': status, 'error': row.get('error') or None, 'alignment': row.get('alignment') or None, 'candidate_path': row.get('candidate_path') or None}

def build_classification_rows(details: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for result in details.get('results', []):
        final_label = 'PASS' if int(result.get('pass_count') or 0) > 0 else 'FAIL'
        rows.append({'task_id': result.get('task_id'), 'class_id': result.get('class_id'), 'function': result.get('function'), 'path_b': result.get('best_sample_path') or result.get('path_b'), 'raw_label': result.get('raw_label'), 'raw_status': result.get('raw_status'), 'final_label': final_label, 'decision_stage': 'pass@5', 'passed': final_label == 'PASS', 'sample_count': result.get('sample_count'), 'pass_count': result.get('pass_count'), 'pass_at_1': result.get('pass_at_1'), 'pass_at_3': result.get('pass_at_3'), 'pass_at_5': result.get('pass_at_5'), 'best_sample_index': result.get('best_sample_index'), 'best_sample_path': result.get('best_sample_path'), 'sample_statuses': sample_statuses(result), 'failure_note': None if final_label == 'PASS' else 'evaluation incomplete; result is undetermined' if final_label == 'ERROR' else 'all samples failed', 'error_summary': build_error_summary(result)})
    return rows

def sample_statuses(result: dict[str, Any]) -> list[dict[str, Any]]:
    statuses = []
    for sample in result.get('samples', []) or []:
        statuses.append({'sample_index': sample.get('sample_index'), 'candidate_path': sample.get('candidate_path'), 'status': sample.get('sample_status', infer_sample_status(sample)), 'label': sample.get('sample_label'), 'cases': [{'label': case.get('label'), 'status': case.get('status'), 'jsd': case.get('jsd'), 'tvd': case.get('tvd'), 'classical_fidelity': case.get('classical_fidelity')} for case in sample.get('cases', []) or []]})
    return statuses

def build_error_summary(result: dict[str, Any]) -> dict[str, Any]:
    errors = []
    setup_error = result.get('setup_error')
    if setup_error:
        errors.append({'case': 'SETUP', 'error': str(setup_error)})
    for sample in result.get('samples', []) or []:
        for case in sample.get('cases', []) or []:
            error = case.get('error')
            if error:
                errors.append({'sample_index': sample.get('sample_index'), 'case': str(case.get('label')), 'error': str(error)})
    return {'raw': errors} if errors else {}

def build_fail_samples(classification: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details.get('results', [])}
    samples = []
    for row in classification:
        if row.get('final_label') != 'FAIL':
            continue
        task_id = int(row['task_id'])
        samples.append({'task_id': task_id, 'class_id': row.get('class_id'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(task_id)})
    return samples

def build_error_samples(classification: list[dict[str, Any]], details: dict[str, Any]) -> list[dict[str, Any]]:
    by_task = {int(result['task_id']): result for result in details.get('results', [])}
    return [{'task_id': row['task_id'], 'class_id': row.get('class_id'), 'function': row.get('function'), 'path_b': row.get('path_b'), 'failure_note': row.get('failure_note'), 'raw': by_task.get(int(row['task_id']))} for row in classification if row.get('final_label') == 'ERROR']

def build_summary(classification: list[dict[str, Any]]) -> dict[str, Any]:
    task_total = len(classification)
    task_raw_pass = sum((1 for row in classification if int(row.get('pass_count') or 0) > 0))
    task_error = sum((1 for row in classification if row.get('raw_status') == 'ERROR'))
    sample_total = sum((int(row.get('sample_count') or 0) for row in classification))
    sample_pass = sum((int(row.get('pass_count') or 0) for row in classification))
    all_sample_statuses = [status for row in classification for status in row.get('sample_statuses') or []]
    sample_error = sum((1 for item in all_sample_statuses if item.get('status') == 'ERROR'))
    sample_fail = sum((1 for item in all_sample_statuses if item.get('status') == 'FAIL'))
    pass_at_1_values = [float(row['pass_at_1']) for row in classification if row.get('pass_at_1') is not None]
    pass_at_3_values = [float(row['pass_at_3']) for row in classification if row.get('pass_at_3') is not None]
    pass_at_5_values = [float(row['pass_at_5']) for row in classification if row.get('pass_at_5') is not None]
    pass_at_1_sum = sum(pass_at_1_values)
    pass_at_3_sum = sum(pass_at_3_values)
    pass_at_5_sum = sum(pass_at_5_values)
    return {'task_total': task_total, 'task_RAW_PASS': task_raw_pass, 'task_FAIL': sum((1 for row in classification if row.get('raw_status') == 'FAIL')), 'task_ERROR': task_error, 'sample_total': sample_total, 'sample_PASS': sample_pass, 'sample_FAIL': sample_fail, 'sample_ERROR': sample_error, 'pass_at_1_sum': pass_at_1_sum, 'pass_at_3_sum': pass_at_3_sum, 'pass_at_5_sum': pass_at_5_sum, 'pass_at_1': None if not pass_at_1_values else pass_at_1_sum / len(pass_at_1_values), 'pass_at_3': None if not pass_at_3_values else pass_at_3_sum / len(pass_at_3_values), 'pass_at_5': None if not pass_at_5_values else pass_at_5_sum / len(pass_at_5_values), 'pass_at_1_defined_task_count': len(pass_at_1_values), 'pass_at_3_defined_task_count': len(pass_at_3_values), 'pass_at_k_defined_task_count': len(pass_at_5_values)}

def build_raw_text_report(details: dict[str, Any]) -> str:
    rows = []
    for result in details.get('results', []):
        task_label = f'code{result['task_id']}'
        samples = result.get('samples', []) or []
        rows.append([task_label, str(result.get('sample_count') or 0), str(result.get('pass_count') or 0), format_metric(result.get('pass_at_1')), format_metric(result.get('pass_at_3')), format_metric(result.get('pass_at_5')), build_task_note(result)])
    headers = ['code', 'samples', 'c', 'pass@1', 'pass@3', 'pass@5', 'note']
    table = format_table(headers, rows)
    summary = details.get('summary', {})
    return '\n'.join(['Cross-language Class 1 raw-style evaluation report', f'model: {details.get('model')}', f'framework: {details.get('framework')}', f'dir_a: {details.get('dir_a')}', f'dir_b: {details.get('dir_b')}', f'thresholds: jsd <= {details['thresholds']['jsd_max']}, tvd <= {details['thresholds']['tvd_max']}, classical_fidelity >= {details['thresholds']['classical_fidelity_min']}', '', table, '', 'overall summary:', f'task_RAW_PASS: {summary.get('task_RAW_PASS', 0)} / {summary.get('task_total', 0)}', f'task_FAIL: {summary.get('task_FAIL', 0)} / {summary.get('task_total', 0)}', f'task_ERROR: {summary.get('task_ERROR', 0)} / {summary.get('task_total', 0)}', f'sample_PASS: {summary.get('sample_PASS', 0)} / {summary.get('sample_total', 0)}', f'sample_FAIL: {summary.get('sample_FAIL', 0)} / {summary.get('sample_total', 0)}', f'sample_ERROR: {summary.get('sample_ERROR', 0)} / {summary.get('sample_total', 0)}', f'pass@1: {format_rate(summary.get('pass_at_1'))}', f'pass@3: {format_rate(summary.get('pass_at_3'))}', f'pass@5: {format_rate(summary.get('pass_at_5'))}', f'pass@k defined tasks: @1={summary.get('pass_at_1_defined_task_count', 0)}, @3={summary.get('pass_at_3_defined_task_count', 0)}, @5={summary.get('pass_at_k_defined_task_count', 0)}', ''])

def build_task_note(result: dict[str, Any]) -> str:
    if result.get('setup_error'):
        return summarize_error_note(result.get('setup_error'))
    if int(result.get('pass_count') or 0) > 0:
        return ''
    for sample in result.get('samples', []) or []:
        for case in sample.get('cases', []) or []:
            note = summarize_error_note(case.get('error'))
            if note:
                return note
    if not result.get('samples'):
        return 'No samples'
    return 'All samples failed'

def format_table(headers: list[str], rows: list[list[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, value in enumerate(row):
            widths[index] = max(widths[index], len(value))
    lines = [' | '.join((header.ljust(widths[index]) for index, header in enumerate(headers))), '-+-'.join(('-' * width for width in widths))]
    for row in rows:
        lines.append(' | '.join((value.ljust(widths[index]) for index, value in enumerate(row))))
    return '\n'.join(lines)

def summarize_error_note(error: Any, max_length: int=160) -> str:
    if not error:
        return ''
    text = str(error).replace('\r\n', '\n').replace('\r', '\n')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return ''
    traceback_start = next((index for index, line in enumerate(lines) if line.startswith('Traceback ')), None)
    if traceback_start is not None:
        summary = lines[-1]
    else:
        summary = lines[0]
    summary = re.sub('\\s+', ' ', summary).strip()
    if len(summary) > max_length:
        return summary[:max_length - 3].rstrip() + '...'
    return summary

def build_environment(framework: str) -> dict[str, Any]:
    packages = {'qiskit': package_version('qiskit'), 'qiskit-aer': package_version('qiskit-aer'), 'qiskit-ibm-runtime': package_version('qiskit-ibm-runtime'), 'cirq': package_version('cirq'), 'pyqpanda3': package_version('pyqpanda3'), 'pyqpanda': package_version('pyqpanda')}
    return {'python': platform.python_version(), 'platform': platform.platform(), 'framework': framework, 'packages': packages}

def build_environment_text(environment: dict[str, Any]) -> str:
    lines = [f'python: {environment.get('python')}', f'platform: {environment.get('platform')}', f'framework: {environment.get('framework')}', 'packages:']
    for name, version in (environment.get('packages') or {}).items():
        lines.append(f'- {name}: {version}')
    return '\n'.join(lines) + '\n'

def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None

def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')

def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + '\n')

def write_summary_csv(path: Path, summary: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='\n') as handle:
        writer = csv.writer(handle)
        writer.writerow(['metric', 'value'])
        for metric, value in build_summary_csv_rows(summary):
            writer.writerow([metric, value])

def build_summary_csv_rows(summary: dict[str, Any]) -> list[tuple[str, str]]:
    task_total = int(summary.get('task_total') or summary.get('total') or 0)
    task_raw_pass = int(summary.get('task_RAW_PASS') or summary.get('RAW_PASS') or 0)
    task_fail = int(summary.get('task_FAIL') or summary.get('raw_fail') or 0)
    task_error = int(summary.get('task_ERROR') or 0)
    sample_total = int(summary.get('sample_total') or 0)
    sample_pass = int(summary.get('sample_PASS') or 0)
    sample_fail = int(summary.get('sample_FAIL') or 0)
    sample_error = int(summary.get('sample_ERROR') or 0)
    return [('task_RAW_PASS', format_count(task_raw_pass, task_total)), ('task_FAIL', format_count(task_fail, task_total)), ('task_ERROR', format_count(task_error, task_total)), ('sample_PASS', format_count(sample_pass, sample_total)), ('sample_FAIL', format_count(sample_fail, sample_total)), ('sample_ERROR', format_count(sample_error, sample_total)), ('pass@1_defined_task_count', str(summary.get('pass_at_1_defined_task_count', 0))), ('pass@3_defined_task_count', str(summary.get('pass_at_3_defined_task_count', 0))), ('pass@5_defined_task_count', str(summary.get('pass_at_k_defined_task_count', 0))), ('pass@1', format_rate(summary.get('pass_at_1'))), ('pass@3', format_rate(summary.get('pass_at_3'))), ('pass@5', format_rate(summary.get('pass_at_5')))]

def format_count(value: int, total: int) -> str:
    return f'{value} / {total}'

def format_rate(value: Any) -> str:
    if value in ('', None):
        return ''
    return f'{float(value):.4f}'

def write_metrics_xlsx(path: Path, details: dict[str, Any]) -> None:
    summary_headers, summary_rows = build_metrics_summary_rows(details)
    sample_headers, sample_rows = build_metrics_sample_rows(details)
    case_headers, case_rows = build_metrics_case_rows(details)
    write_xlsx(path, [('Summary', summary_headers, summary_rows), ('Samples', sample_headers, sample_rows), ('Cases', case_headers, case_rows)])

def build_metrics_summary_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'samples', 'c', 'pass@1', 'pass@3', 'pass@5', 'note']
    rows = []
    for result in details.get('results', []) or []:
        rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), result.get('sample_count'), result.get('pass_count'), result.get('pass_at_1'), result.get('pass_at_3'), result.get('pass_at_5'), build_task_note(result)])
    return (headers, rows)

def build_metrics_sample_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'candidate_file', 'sample_pass', 'sample_status', 'case_count', 'pass_case_count', 'fail_case_count', 'error_case_count', 'max_jsd', 'max_tvd', 'min_classical_fidelity', 'jsd_threshold', 'tvd_threshold', 'fidelity_threshold', 'note']
    thresholds = details.get('thresholds') or {}
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            cases = sample.get('cases', []) or []
            pass_case_count = sum((1 for case in cases if case.get('status') == 'PASS'))
            fail_case_count = sum((1 for case in cases if case.get('status') == 'FAIL'))
            error_case_count = sum((1 for case in cases if case.get('status') == 'ERROR'))
            numeric_jsd = [case.get('jsd') for case in cases if case.get('jsd') is not None]
            numeric_tvd = [case.get('tvd') for case in cases if case.get('tvd') is not None]
            numeric_fidelity = [case.get('classical_fidelity') for case in cases if case.get('classical_fidelity') is not None]
            note = '; '.join((summarize_error_note(case.get('error')) for case in cases if case.get('error')))
            rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), Path(str(sample.get('candidate_path') or '')).name, bool(sample.get('sample_pass')), sample.get('sample_status', infer_sample_status(sample)), len(cases), pass_case_count, fail_case_count, error_case_count, max(numeric_jsd) if numeric_jsd else None, max(numeric_tvd) if numeric_tvd else None, min(numeric_fidelity) if numeric_fidelity else None, thresholds.get('jsd_max'), thresholds.get('tvd_max'), thresholds.get('classical_fidelity_min'), summarize_error_note(note)])
    return (headers, rows)

def build_metrics_case_rows(details: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
    headers = ['model', 'framework', 'code', 'task_id', 'function', 'sample_index', 'case', 'repeat', 'status', 'judgeable', 'alignment', 'jsd', 'jsd_threshold', 'jsd_pass', 'tvd', 'tvd_threshold', 'tvd_pass', 'classical_fidelity', 'fidelity_threshold', 'fidelity_pass', 'error', 'candidate_path']
    thresholds = details.get('thresholds') or {}
    jsd_threshold = thresholds.get('jsd_max')
    tvd_threshold = thresholds.get('tvd_max')
    fidelity_threshold = thresholds.get('classical_fidelity_min')
    rows = []
    for result in details.get('results', []) or []:
        for sample in result.get('samples', []) or []:
            for case in sample.get('cases', []) or []:
                jsd = case.get('jsd')
                tvd = case.get('tvd')
                fidelity = case.get('classical_fidelity')
                rows.append([details.get('model'), details.get('framework'), f'code{result.get('task_id')}', result.get('task_id'), result.get('function'), sample.get('sample_index'), case.get('label'), case.get('repeat'), case.get('status'), case.get('status') in {'PASS', 'FAIL'}, case.get('alignment'), jsd, jsd_threshold, None if jsd is None else jsd <= jsd_threshold, tvd, tvd_threshold, None if tvd is None else tvd <= tvd_threshold, fidelity, fidelity_threshold, None if fidelity is None else fidelity >= fidelity_threshold, case.get('error'), case.get('candidate_path')])
    return (headers, rows)

def write_xlsx(path: Path, sheets: list[tuple[str, list[str], list[list[Any]]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr('[Content_Types].xml', xlsx_content_types(len(sheets)))
        archive.writestr('_rels/.rels', xlsx_root_rels())
        archive.writestr('xl/workbook.xml', xlsx_workbook([sheet[0] for sheet in sheets]))
        archive.writestr('xl/_rels/workbook.xml.rels', xlsx_workbook_rels(len(sheets)))
        archive.writestr('xl/styles.xml', xlsx_styles())
        for index, (_, headers, rows) in enumerate(sheets, start=1):
            archive.writestr(f'xl/worksheets/sheet{index}.xml', xlsx_sheet(headers, rows))

def xlsx_content_types(sheet_count: int) -> str:
    overrides = '\n'.join((f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for index in range(1, sheet_count + 1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n<Default Extension="xml" ContentType="application/xml"/>\n<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>\n<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>\n{overrides}\n</Types>'

def xlsx_root_rels() -> str:
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>\n</Relationships>'

def xlsx_workbook(sheet_names: list[str]) -> str:
    sheets_xml = '\n'.join((f'<sheet name="{escape(sheet_name)}" sheetId="{index}" r:id="rId{index}"/>' for index, sheet_name in enumerate(sheet_names, start=1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">\n<sheets>\n{sheets_xml}\n</sheets>\n</workbook>'

def xlsx_workbook_rels(sheet_count: int) -> str:
    rels = '\n'.join((f'<Relationship Id="rId{index}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{index}.xml"/>' for index in range(1, sheet_count + 1)))
    rels += f'\n<Relationship Id="rId{sheet_count + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n{rels}\n</Relationships>'

def xlsx_styles() -> str:
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">\n<fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>\n<fills count="1"><fill><patternFill patternType="none"/></fill></fills>\n<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>\n<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>\n<cellXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/></cellXfs>\n</styleSheet>'

def xlsx_sheet(headers: list[str], rows: list[list[Any]]) -> str:
    all_rows = [headers, *rows]
    row_xml = '\n'.join((f'<row r="{row_index}">' + ''.join((xlsx_cell(row_index, column_index, value) for column_index, value in enumerate(row, start=1))) + '</row>' for row_index, row in enumerate(all_rows, start=1)))
    return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">\n<sheetData>\n{row_xml}\n</sheetData>\n</worksheet>'

def xlsx_cell(row_index: int, column_index: int, value: Any) -> str:
    cell_ref = f'{xlsx_column_name(column_index)}{row_index}'
    if value in ('', None):
        return f'<c r="{cell_ref}"/>'
    if isinstance(value, bool):
        return f'<c r="{cell_ref}" t="b"><v>{(1 if value else 0)}</v></c>'
    if isinstance(value, (int, float)) and (not isinstance(value, bool)) and math.isfinite(float(value)):
        return f'<c r="{cell_ref}"><v>{format_metric(value)}</v></c>'
    text = escape(str(value), {'"': '&quot;'})
    return f'<c r="{cell_ref}" t="inlineStr"><is><t>{text}</t></is></c>'

def xlsx_column_name(index: int) -> str:
    name = ''
    while index:
        index, remainder = divmod(index - 1, 26)
        name = chr(ord('A') + remainder) + name
    return name

def to_float_or_none(value: Any) -> float | None:
    if value in ('', None):
        return None
    return float(value)

def to_int_or_none(value: Any) -> int | None:
    if value in ('', None):
        return None
    return int(value)

def format_metric(value: Any) -> str:
    if value in ('', None):
        return ''
    number = float(value)
    return f'{number:.12g}'

def resolve_reports_dir(raw_reports_dir: str | None, models: list[str]) -> Path:
    if raw_reports_dir:
        return Path(raw_reports_dir)
    return DEFAULT_REPORTS_DIR

def join_key(prefix: str, key: str) -> str:
    return f'{prefix}.{key}' if prefix else key

def pick_best_alignment(reference: dict[str, float], candidate: dict[str, float]) -> tuple[str, dict[str, float]]:
    candidates: list[tuple[str, dict[str, float]]] = []

    def add(name: str, dist: dict[str, float]) -> None:
        signature = json.dumps(sorted(dist.items()), sort_keys=True)
        if all((json.dumps(sorted(existing.items()), sort_keys=True) != signature for _, existing in candidates)):
            candidates.append((name, dist))
    add('identity', candidate)
    ref_binary, width = binary_width(reference)
    if ref_binary:
        padded = pad_binary_keys(candidate, width)
        if padded is not None:
            add('pad_binary', padded)
        decimal = decimal_keys_to_binary(candidate, width)
        if decimal is not None:
            add('decimal_to_binary', decimal)
    expanded = list(candidates)
    for name, dist in expanded:
        cand_binary, cand_width = binary_width(dist)
        if ref_binary and cand_binary and (cand_width == width):
            add(f'{name}+bit_reverse', reverse_binary_keys(dist))
    scored = [(name, compare_distributions(reference, dist)) for name, dist in candidates]
    scored.sort(key=lambda item: (-item[1]['classical_fidelity'], item[1]['jsd'], item[1]['tvd']))
    return scored[0]

def compare_distributions(dist_a: dict[str, float], dist_b: dict[str, float]) -> dict[str, float]:
    dist_a, dist_b = canonicalize_distribution_pair(dist_a, dist_b)
    keys = sorted(set(dist_a) | set(dist_b))
    p = normalize_vector([dist_a.get(key, 0.0) for key in keys])
    q = normalize_vector([dist_b.get(key, 0.0) for key in keys])
    tvd = 0.5 * sum((abs(left - right) for left, right in zip(p, q)))
    midpoint = [(left + right) / 2.0 for left, right in zip(p, q)]
    jsd = 0.5 * kl_divergence_base2(p, midpoint) + 0.5 * kl_divergence_base2(q, midpoint)
    fidelity = sum((math.sqrt(max(left, 0.0) * max(right, 0.0)) for left, right in zip(p, q))) ** 2
    return {'jsd': float(jsd), 'tvd': float(tvd), 'classical_fidelity': float(fidelity)}

def normalize_vector(values: list[float]) -> list[float]:
    clipped = [max(float(value), 0.0) for value in values]
    total = sum(clipped)
    if total <= 0:
        raise ValueError('Distribution has no positive probability mass.')
    return [value / total for value in clipped]

def kl_divergence_base2(p: list[float], q: list[float]) -> float:
    total = 0.0
    for left, right in zip(p, q):
        if left == 0.0:
            continue
        if right == 0.0:
            return math.inf
        total += left * math.log(left / right, 2)
    return total

def canonicalize_distribution_pair(dist_a: dict[str, float], dist_b: dict[str, float]) -> tuple[dict[str, float], dict[str, float]]:
    keys = list(dist_a) + list(dist_b)
    widths: dict[str, int] = {}
    for key in keys:
        parsed = parse_binary_like_key(key)
        if parsed is None:
            continue
        prefix, _, width = parsed
        widths[prefix] = max(widths.get(prefix, 1), width)
    return (canonicalize_distribution_keys(dist_a, widths), canonicalize_distribution_keys(dist_b, widths))

def canonicalize_distribution_keys(dist: dict[str, float], widths: dict[str, int]) -> dict[str, float]:
    canonical: dict[str, float] = {}
    for key, value in dist.items():
        parsed = parse_binary_like_key(key)
        if parsed is None:
            canonical_key = key
        else:
            prefix, number, width = parsed
            final_width = max(widths.get(prefix, width), 1)
            rendered = format(number, f'0{final_width}b')
            canonical_key = join_key(prefix, rendered) if prefix else rendered
        canonical[canonical_key] = canonical.get(canonical_key, 0.0) + value
    return canonical

def parse_binary_like_key(key: str) -> tuple[str, int, int] | None:
    prefix, _, tail = key.rpartition('.')
    if tail.startswith('int:'):
        raw = tail[4:]
        if raw.isdecimal():
            number = int(raw)
            return (prefix, number, max(1, number.bit_length()))
    compact = tail.replace(' ', '')
    if compact and all((char in '01' for char in compact)):
        return (prefix, int(compact, 2), len(compact))
    return None

def binary_width(dist: dict[str, float]) -> tuple[bool, int]:
    if not dist:
        return (False, 0)
    widths = set()
    for key in dist:
        if not key or any((char not in '01' for char in key)):
            return (False, 0)
        widths.add(len(key))
    if len(widths) != 1:
        return (False, 0)
    return (True, next(iter(widths)))

def pad_binary_keys(dist: dict[str, float], width: int) -> dict[str, float] | None:
    converted: dict[str, float] = {}
    for key, value in dist.items():
        if not key or any((char not in '01' for char in key)) or len(key) > width:
            return None
        padded = key.zfill(width)
        converted[padded] = converted.get(padded, 0.0) + value
    return converted

def decimal_keys_to_binary(dist: dict[str, float], width: int) -> dict[str, float] | None:
    converted: dict[str, float] = {}
    max_value = 2 ** width - 1
    for key, value in dist.items():
        if not re.fullmatch('\\d+', key):
            return None
        integer = int(key)
        if integer > max_value:
            return None
        bitstring = format(integer, f'0{width}b')
        converted[bitstring] = converted.get(bitstring, 0.0) + value
    return converted

def reverse_binary_keys(dist: dict[str, float]) -> dict[str, float]:
    reversed_dist: dict[str, float] = {}
    for key, value in dist.items():
        new_key = key[::-1]
        reversed_dist[new_key] = reversed_dist.get(new_key, 0.0) + value
    return reversed_dist
