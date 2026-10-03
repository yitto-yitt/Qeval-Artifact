# EVAL_META: task_id=4, framework=qpanda, class=3
from pyqpanda3.core import *

def create_unitary_from_matrix():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    circuit = QCircuit()
    circuit << CNOT(q[1], q[0]) << X(q[1])
    return circuit
