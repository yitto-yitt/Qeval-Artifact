# EVAL_META: task_id=59, framework=qpanda2, class=3
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)
atexit.register(machine.finalize)

def create_cz_gate():
    circuit = QCircuit()
    circuit << H(qubits[1])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << H(qubits[1])
    return circuit
