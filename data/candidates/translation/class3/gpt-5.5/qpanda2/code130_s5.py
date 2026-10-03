# EVAL_META: task_id=130, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
_qubits = machine.qAlloc_many(5)
atexit.register(machine.finalize)

def inv_circuit(n):
    if n < 5:
        raise IndexError("qubit index out of range")

    circuit = QCircuit()
    circuit.insert(CNOT(_qubits[2], _qubits[4]))
    circuit.insert(CNOT(_qubits[1], _qubits[3]))
    circuit.insert(H(_qubits[2]))
    circuit.insert(H(_qubits[1]))
    return circuit
