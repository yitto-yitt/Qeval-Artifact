# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, H, CP

def qft_no_swaps(num_qubits):
    qc = QCircuit()
    for j in range(num_qubits):
        qj = num_qubits - 1 - j
        qc.insert(H(qj))
        for k in range(2, num_qubits - j + 1):
            qk = qj - (k - 1)
            angle = -2.0 * 3.141592653589793 / (2 ** k)
            qc.insert(CP(angle, qk, qj))
    return qc
