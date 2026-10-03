# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda import *
from numpy import pi

def create_ch_gate():
    machine = init(QMachineType.CPU)
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit.insert(RY(qubits[1], pi/4))
    circuit.insert(CNOT(qubits[0], qubits[1]))
    circuit.insert(RY(qubits[1], -pi/4))
    return circuit
