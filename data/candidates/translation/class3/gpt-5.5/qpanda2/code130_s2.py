# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
from pyqpanda import CPUQVM, QCircuit, H, CNOT

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)

def inv_circuit(n):
    if n < 5:
        raise ValueError("n must be at least 5")
    if n > len(_qubits):
        raise ValueError("n exceeds globally allocated qubits")

    qc = QCircuit()
    qc << CNOT(_qubits[2], _qubits[4])
    qc << CNOT(_qubits[1], _qubits[3])
    qc << H(_qubits[2])
    qc << H(_qubits[1])
    return qc
