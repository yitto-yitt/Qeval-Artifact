# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(64)
atexit.register(machine.finalize)

def inv_circuit(n):
    if n < 5:
        raise IndexError("qubit index out of range")
    if n > len(_qubits):
        raise ValueError("n exceeds globally allocated qubit count")

    circuit = QCircuit()
    circuit << CNOT(_qubits[2], _qubits[4])
    circuit << CNOT(_qubits[1], _qubits[3])
    circuit << H(_qubits[2])
    circuit << H(_qubits[1])
    return circuit
