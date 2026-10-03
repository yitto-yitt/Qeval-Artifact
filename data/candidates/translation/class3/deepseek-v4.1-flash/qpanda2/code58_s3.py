# EVAL_META: task_id=58, framework=qpanda2, class=3
from pyqpanda import *
from numpy import pi

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(2)

def create_ch_gate():
    circuit = QCircuit()
    circuit << RY(qubits[1], pi/4) << CNOT(qubits[0], qubits[1]) << RY(qubits[1], -pi/4)
    return circuit

machine.finalize()
