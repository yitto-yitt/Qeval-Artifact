# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CP, SWAP, dagger

def qft_no_swaps(num_qubits):
    qft = QCircuit()
    for j in range(num_qubits):
        qft << H(j)
        for k in range(j + 1, num_qubits):
            qft << CP(j, k, 3.141592653589793 / (2 ** (k - j)))
    inv_qft = dagger(qft)
    return inv_qft
