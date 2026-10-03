# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT


def qft_no_swaps(num_qubits):
    # Create a QFT circuit
    qft_circ = QFT(num_qubits, inverse=True, do_swaps=False)
    return qft_circ
