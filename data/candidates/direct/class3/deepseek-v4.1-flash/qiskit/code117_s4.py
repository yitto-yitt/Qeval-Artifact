# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import CXGate
from qiskit.quantum_info import Operator

try:
    from qiskit.synthesis import TwoQubitBasisDecomposer
except ImportError:
    from qiskit.transpiler.synthesis import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    if not isinstance(unitary, Operator):
        unitary = Operator(unitary)
    return decomposer(unitary)
