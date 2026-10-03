# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import CXGate
from qiskit.synthesis import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(np.asarray(unitary, dtype=complex))
