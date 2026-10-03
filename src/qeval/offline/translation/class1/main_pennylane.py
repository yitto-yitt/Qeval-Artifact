import argparse
import importlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
import main as base
PENNYLANE_FRAMEWORK = 'pennylane'
PENNYLANE_PACKAGE = 'pennylane==0.45.1'
BASE_BUILD_DJ_ORACLE = base.build_dj_oracle
BASE_EXTRACT_DISTRIBUTION_LIKE = base.extract_distribution_like
BASE_EVALUATE = base.evaluate

class PennyLaneDeutschJozsaOracle:

    def __init__(self, case_label: str) -> None:
        if case_label not in {'constant_oracle', 'balanced_oracle'}:
            raise ValueError(f'Unknown oracle case: {case_label}')
        self.case_label = case_label
        self.num_qubits = 3
        self.num_wires = 3
        self.wires = tuple(range(3))

    def __call__(self, wires: Any=None) -> None:
        import pennylane as qml
        labels = tuple(self.wires if wires is None else wires)
        if len(labels) != self.num_qubits:
            raise ValueError(f'Expected {self.num_qubits} oracle wires, got {len(labels)}')
        if self.case_label == 'balanced_oracle':
            qml.CNOT(wires=[labels[0], labels[2]])
            qml.CNOT(wires=[labels[1], labels[2]])

def build_dj_oracle(framework: str, case_label: str) -> Any:
    if framework != PENNYLANE_FRAMEWORK:
        return BASE_BUILD_DJ_ORACLE(framework, case_label)
    return PennyLaneDeutschJozsaOracle(case_label)

def build_environment(framework: str) -> dict[str, Any]:
    packages = {'qiskit': base.package_version('qiskit'), 'qiskit-aer': base.package_version('qiskit-aer'), 'qiskit-ibm-runtime': base.package_version('qiskit-ibm-runtime'), 'cirq': base.package_version('cirq'), 'pyqpanda3': base.package_version('pyqpanda3'), 'pennylane': base.package_version('pennylane')}
    return {'python': base.platform.python_version(), 'platform': base.platform.platform(), 'framework': framework, 'packages': packages}

def patch_base_module() -> None:
    base.FRAMEWORK_NAMES[PENNYLANE_FRAMEWORK] = 'PennyLane'
    base.FRAMEWORK_PACKAGES[PENNYLANE_FRAMEWORK] = [PENNYLANE_PACKAGE]
    base.build_dj_oracle = build_dj_oracle
    base.build_environment = build_environment
    base.extract_distribution_like = extract_distribution_like
    base.evaluate = evaluate
    base.run_case_subprocess = run_case_subprocess

def extract_distribution_like(value: Any, owner: Any | None=None) -> Any | None:
    if is_pennylane_qnode(owner):
        return None
    if is_numpy_array_value(value):
        return pennylane_value_to_distribution_like(value)
    direct = BASE_EXTRACT_DISTRIBUTION_LIKE(value, owner)
    if direct is not None:
        return direct
    return pennylane_value_to_distribution_like(value)

def is_numpy_array_value(value: Any) -> bool:
    try:
        import numpy as np
    except Exception:
        return False
    return isinstance(value, np.ndarray)

def pennylane_value_to_distribution_like(value: Any) -> Any | None:
    if value is None or callable(value) or is_pennylane_measurement_process(value):
        return None
    array = as_numpy_array(value)
    if array is None:
        return None
    return numpy_array_to_distribution_like(array)

def as_numpy_array(value: Any) -> Any | None:
    if isinstance(value, (str, bytes, bytearray)):
        return None
    try:
        import numpy as np
    except Exception:
        return None
    if isinstance(value, np.ndarray):
        return value
    if not hasattr(value, '__array__') and (not hasattr(value, 'shape')):
        return None
    try:
        return np.asarray(value)
    except Exception:
        return None

def numpy_array_to_distribution_like(array: Any) -> Any | None:
    import numpy as np
    if array.ndim == 0:
        scalar = array.item()
        if base.is_number(scalar):
            return {'value': float(scalar)}
        return None
    if np.iscomplexobj(array):
        amplitudes = np.asarray(array).reshape(-1)
        probabilities = np.abs(amplitudes) ** 2
        total = float(np.sum(probabilities))
        if total <= 0 or not np.isfinite(total):
            return None
        return {index: float(probability) for index, probability in enumerate(probabilities)}
    integer_like = array.dtype.kind in {'b', 'i', 'u'}
    real_array = safe_real_array(array)
    if real_array is None:
        return None
    if real_array.ndim == 2 and array_contains_bits(real_array):
        return sample_rows_to_distribution(real_array)
    if real_array.ndim == 1:
        is_statevector = looks_like_statevector(real_array)
        is_probability_vector = looks_like_probability_vector(real_array)
        if integer_like:
            if is_probability_vector:
                return None
            return one_dimensional_integer_samples_to_distribution(real_array)
        if is_statevector and is_probability_vector:
            state_probabilities = np.abs(real_array) ** 2
            if np.allclose(state_probabilities, real_array, atol=1e-09):
                return {index: float(probability) for index, probability in enumerate(real_array)}
            return None
        if is_statevector:
            probabilities = np.abs(real_array) ** 2
            return {index: float(probability) for index, probability in enumerate(probabilities)}
        if is_probability_vector:
            return {index: float(probability) for index, probability in enumerate(real_array)}
        if values_are_close_to_integers(real_array):
            return one_dimensional_integer_samples_to_distribution(real_array)
    return None

def safe_real_array(array: Any) -> Any | None:
    try:
        import numpy as np
        return np.asarray(array, dtype=float)
    except Exception:
        return None

def looks_like_statevector(array: Any) -> bool:
    import numpy as np
    if array.ndim != 1 or array.size == 0:
        return False
    norm = float(np.sum(np.abs(array) ** 2))
    return is_power_of_two(int(array.size)) and abs(norm - 1.0) <= 1e-06

def looks_like_probability_vector(array: Any) -> bool:
    import numpy as np
    if array.ndim != 1 or array.size == 0:
        return False
    if not np.all(np.isfinite(array)):
        return False
    if np.any(array < -1e-09):
        return False
    total = float(np.sum(array))
    return total > 0 and abs(total - 1.0) <= 1e-06

def values_are_close_to_integers(array: Any) -> bool:
    import numpy as np
    if array.ndim != 1 or array.size == 0:
        return False
    rounded = np.rint(array)
    return bool(np.all(np.isfinite(array)) and np.allclose(array, rounded, atol=1e-09))

def array_contains_bits(array: Any) -> bool:
    import numpy as np
    if array.size == 0:
        return False
    rounded = np.rint(array)
    return bool(np.allclose(array, rounded, atol=1e-09) and np.all(np.isin(rounded, [0.0, 1.0])))

def one_dimensional_integer_samples_to_distribution(array: Any) -> dict[str, float]:
    import numpy as np
    rounded = np.rint(array).astype(int).tolist()
    counts: dict[str, float] = {}
    for item in rounded:
        key = base.stable_key(item)
        counts[key] = counts.get(key, 0.0) + 1.0
    return counts

def sample_rows_to_distribution(array: Any) -> dict[str, float]:
    import numpy as np
    rounded = np.rint(array).astype(int)
    counts: dict[str, float] = {}
    for row in rounded:
        key = ''.join((str(int(bit)) for bit in np.asarray(row).tolist()))
        counts[key] = counts.get(key, 0.0) + 1.0
    return counts

def is_power_of_two(value: int) -> bool:
    return value > 0 and value & value - 1 == 0

def is_pennylane_qnode(value: Any) -> bool:
    if not callable(value):
        return False
    class_name = value.__class__.__name__
    module_name = value.__class__.__module__
    return class_name == 'QNode' or (module_name.startswith('pennylane') and 'qnode' in class_name.lower())

def is_pennylane_measurement_process(value: Any) -> bool:
    class_name = value.__class__.__name__
    module_name = value.__class__.__module__
    if not module_name.startswith('pennylane'):
        return False
    return class_name.endswith('MP') or 'Measurement' in class_name

def run_case_subprocess(*, module_path: Path, function_name: str, task_id: int, framework: str, case_label: str, repeats: int, timeout: float, python_exe: Path | None=None) -> dict[str, Any]:
    module_label = Path(module_path).stem
    print(f'[run] {framework} {module_label} case={case_label} repeats={repeats}', flush=True)
    cmd = [str(python_exe or sys.executable), str(Path(__file__).resolve()), '_run_case', '--module', str(module_path), '--function-name', function_name, '--task-id', str(task_id), '--framework', framework, '--case', case_label, '--repeats', str(repeats)]
    try:
        proc = subprocess.run(cmd, cwd=str(base.WORKSPACE_DIR), capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired:
        print(f'[error] {framework} {module_label} case={case_label}: timed out after {timeout} seconds', flush=True)
        return {'ok': False, 'error': f'Timed out after {timeout} seconds'}
    if proc.returncode != 0:
        error_text = (proc.stderr or proc.stdout or f'exit code {proc.returncode}').strip()
        print(f'[error] {framework} {module_label} case={case_label}: {base.summarize_error_note(error_text)}', flush=True)
        return {'ok': False, 'error': error_text}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f'[error] {framework} {module_label} case={case_label}: subprocess returned non-JSON stdout', flush=True)
        return {'ok': False, 'error': 'Subprocess returned non-JSON stdout: ' + proc.stdout[:2000]}

def required_modules_for_evaluation(frameworks: list[str]) -> list[str]:
    required = ['qiskit', 'qiskit_aer', 'qiskit_ibm_runtime']
    if PENNYLANE_FRAMEWORK in frameworks:
        required.append('pennylane')
    return required

def import_error_summary(module_name: str, exc: Exception) -> str:
    message = base.summarize_error_note(f'{exc.__class__.__name__}: {exc}', max_length=240)
    return f'- {module_name}: {message}'

def preflight_evaluation_environment(frameworks: list[str]) -> list[str]:
    issues: list[str] = []
    for module_name in required_modules_for_evaluation(frameworks):
        try:
            importlib.import_module(module_name)
        except Exception as exc:
            issues.append(import_error_summary(module_name, exc))
    return issues

def evaluate(args: argparse.Namespace) -> int:
    frameworks = base.parse_frameworks(args.frameworks)
    issues = preflight_evaluation_environment(frameworks)
    if issues:
        print('Evaluation prerequisites are not importable:', file=sys.stderr)
        for issue in issues:
            print(issue, file=sys.stderr)
        return 2
    return BASE_EVALUATE(args)
