# EVAL_META: task_id=145, framework=qiskit, class=3

from qiskit.circuit.library import QFT
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

def qft_inverse(n):
    return QFT(num_qubits=n, approximation_degree=0, inverse=True)


# ==================================================
