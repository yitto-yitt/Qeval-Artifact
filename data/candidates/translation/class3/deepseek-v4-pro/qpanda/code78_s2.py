# EVAL_META: task_id=78, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, H, CP
import math

_qvm = None

def qft_no_swaps(num_qubits):
    global _qvm
    if num_qubits <= 0:
        return QCircuit()
    if _qvm is None:
        _qvm = CPUQVM()
        _qvm.init_qvm()
    qubits = _qvm.qAlloc_many(num_qubits)
    circuit = QCircuit()
    for j in range(num_qubits - 1, -1, -1):
        for k in range(num_qubits - 1, j, -1):
            circuit << CP(qubits[k], qubits[j], -math.pi / (1 << (k - j)))
        circuit << H(qubits[j])
    return circuit
