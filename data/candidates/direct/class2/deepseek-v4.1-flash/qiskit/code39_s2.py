# EVAL_META: task_id=39, framework=qiskit, class=2
import numpy as np
from qiskit.quantum_info import Statevector


def create_uniform_superposition(n):
    dim = 2 ** n
    amp = 1.0 / np.sqrt(dim)
    return Statevector(np.full(dim, amp, dtype=complex))
