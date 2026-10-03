# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def qft_inverse(n):
    return QFT(n, inverse=True)
