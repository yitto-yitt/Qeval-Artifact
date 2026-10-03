# EVAL_META: task_id=118, framework=qpanda2, class=3
from math import pi
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(4)

def create_c3sx_circuit():
    circuit = QCircuit()
    circuit << U1(qubits[2], pi / 4).control([qubits[0], qubits[1]])
    circuit << RX(qubits[3], pi / 2).control([qubits[0], qubits[1], qubits[2]])
    return circuit

machine.finalize()
