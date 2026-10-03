# EVAL_META: task_id=60, framework=qpanda2, class=3
import atexit
from math import pi
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_cy_gate():
    circuit = QCircuit()
    circuit.insert(RZ(qubits[1], -pi / 2))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(RZ(qubits[1], pi / 2))
    return circuit

atexit.register(lambda: machine.finalize())
