# EVAL_META: task_id=117, framework=qiskit, class=3
import numpy as np
from qiskit.synthesis.two_qubit.two_qubit_decompose import TwoQubitBasisDecomposer
from qiskit.circuit.library import CXGate

def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    circuit = decomposer(unitary)
    return circuit
