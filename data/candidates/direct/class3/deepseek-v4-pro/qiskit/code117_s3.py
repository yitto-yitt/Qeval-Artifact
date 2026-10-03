# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import CXGate
from qiskit.synthesis import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    matrix = np.asarray(unitary, dtype=complex)
    decomposer = TwoQubitBasisDecomposer(CXGate())
    circuit = decomposer(matrix, approximate=False)
    return circuit
