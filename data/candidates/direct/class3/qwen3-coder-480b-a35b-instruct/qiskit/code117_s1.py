# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator
from qiskit.synthesis import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate
import numpy as np

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    circuit = decomposer(unitary)
    return circuit
