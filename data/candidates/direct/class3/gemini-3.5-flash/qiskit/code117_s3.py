# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit.circuit.library import CXGate
try:
    from qiskit.synthesis import TwoQubitBasisDecomposer
except ImportError:
    from qiskit.quantum_info.synthesis.two_qubit_decompose import TwoQubitBasisDecomposer

def decompose_unitary(unitary):
    if hasattr(unitary, 'data'):
        matrix = unitary.data
    else:
        matrix = np.asarray(unitary)
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(matrix)
