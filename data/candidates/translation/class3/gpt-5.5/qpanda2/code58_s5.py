# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
from math import pi
import atexit

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = QCircuit()
    circuit << RY(qubits[1], pi / 4)
    circuit << CNOT(qubits[0], qubits[1])
    circuit << RY(qubits[1], -pi / 4)
    return circuit

atexit.register(machine.finalize)
