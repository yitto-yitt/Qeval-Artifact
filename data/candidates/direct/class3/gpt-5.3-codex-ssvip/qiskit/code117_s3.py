# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Operator
from qiskit.synthesis import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    u = np.asarray(unitary, dtype=complex)
    if u.shape != (4, 4):
        raise ValueError("Input unitary must be a 4x4 matrix.")
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(Operator(u))
