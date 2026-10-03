# EVAL_META: task_id=78, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CR

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(32)

def qft_no_swaps(num_qubits):
    if num_qubits > len(_qubits):
        raise ValueError("num_qubits exceeds globally allocated qubits")
    circuit = QCircuit()
    for j in range(num_qubits):
        for k in range(j):
            circuit.insert(CR(_qubits[j], _qubits[k], -math.pi / (2 ** (j - k))))
        circuit.insert(H(_qubits[j]))
    return circuit

atexit.register(machine.finalize)
