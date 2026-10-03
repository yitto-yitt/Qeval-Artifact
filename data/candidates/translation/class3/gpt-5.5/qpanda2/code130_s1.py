# EVAL_META: task_id=130, framework=qpanda2, class=3
from pyqpanda import *
import atexit

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def inv_circuit(n):
    if n < 5:
        raise ValueError("n must be at least 5")
    qc = QCircuit()
    for i in range(1, -1, -1):
        qc << CNOT(_qubits[i + 1], _qubits[i + 3])
    for i in range(1, -1, -1):
        qc << H(_qubits[i + 1])
    return qc
