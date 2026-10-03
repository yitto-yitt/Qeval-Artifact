# EVAL_META: task_id=2, framework=qiskit, class=2
import math
from qiskit.quantum_info import Statevector


def create_bell_statevector() -> Statevector:
    return Statevector([1 / math.sqrt(2), 0, 0, 1 / math.sqrt(2)])
