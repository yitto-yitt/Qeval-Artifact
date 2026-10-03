# EVAL_META: task_id=118, framework=qpanda2, class=3
import math
import atexit
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << U1(qubits[2], math.pi / 4).control([qubits[0], qubits[1]])
    circuit << RX(qubits[3], math.pi / 2).control([qubits[0], qubits[1], qubits[2]])
    return circuit

atexit.register(machine.finalize)
