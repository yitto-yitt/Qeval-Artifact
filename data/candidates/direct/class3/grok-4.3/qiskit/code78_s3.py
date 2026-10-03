# EVAL_META: task_id=78, framework=qiskit, class=3
from qiskit.circuit.library import QFT
def qft_no_swaps(num_qubits):
    return QFT(num_qubits=num_qubits, do_swaps=False, inverse=True)
