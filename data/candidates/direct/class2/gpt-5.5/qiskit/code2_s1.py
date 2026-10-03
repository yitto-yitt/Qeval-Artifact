# EVAL_META: task_id=2, framework=qiskit, class=2
from math import sqrt
from qiskit.quantum_info import Statevector


def create_bell_statevector():
    return Statevector([1 / sqrt(2), 0, 0, 1 / sqrt(2)])
