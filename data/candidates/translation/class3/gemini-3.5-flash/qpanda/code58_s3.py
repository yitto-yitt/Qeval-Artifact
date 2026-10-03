# EVAL_META: task_id=58, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QCircuit, RY, CNOT
from numpy import pi

def create_ch_gate():
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << RY(qubits[1], pi/4) << CNOT(qubits[0], qubits[1]) << RY(qubits[1], -pi/4)
    return circuit
