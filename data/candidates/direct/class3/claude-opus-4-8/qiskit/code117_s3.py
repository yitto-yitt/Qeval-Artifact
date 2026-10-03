# EVAL_META: task_id=117, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import CXGate
from qiskit.synthesis import TwoQubitBasisDecomposer


def decompose_unitary(unitary):
    decomposer = TwoQubitBasisDecomposer(CXGate())
    circuit = decomposer(unitary)
    return circuit
