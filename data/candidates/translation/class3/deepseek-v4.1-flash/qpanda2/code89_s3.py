# EVAL_META: task_id=89, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(3)

def create_controlled_hgate():
    circuit = QCircuit()
    h_gate = QGate("H", qubits[2])
    h_gate.set_control(qubits[0])
    h_gate.set_control(qubits[1])
    circuit << h_gate
    return circuit

machine.finalize()
