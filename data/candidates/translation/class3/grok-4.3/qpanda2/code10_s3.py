# EVAL_META: task_id=10, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
qubits = qAlloc_many(2)

def create_operator():
    circ = QCircuit()
    circ << X(qubits[0]) << X(qubits[1])
    return circ

machine.finalize()
