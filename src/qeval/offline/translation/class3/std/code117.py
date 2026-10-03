# EVAL_META: task_id=117, framework=qiskit, class=3

from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.quantum_info import Operator, random_unitary
from qiskit.circuit.library import CXGate
from qiskit import QuantumCircuit
import numpy as np

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    return decomposer(unitary)


# ==================================================
