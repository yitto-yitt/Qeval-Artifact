# EVAL_META: task_id=145, framework=qiskit, class=3
from qiskit.circuit.library import QFT

def qft_inverse(n):
    """Return the inverse QFT circuit for n qubits."""
    return QFT(num_qubits=n, inverse=True)
