# EVAL_META: task_id=118, framework=qpanda2, class=3
import atexit
from math import pi
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit.insert(T(qubits[2]).control([qubits[0], qubits[1]]))
    circuit.insert(RX(qubits[3], pi / 2).control([qubits[0], qubits[1], qubits[2]]))
    return circuit

atexit.register(machine.finalize)
