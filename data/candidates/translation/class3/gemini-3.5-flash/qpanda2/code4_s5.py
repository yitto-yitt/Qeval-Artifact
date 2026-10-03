# EVAL_META: task_id=4, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(2)

def create_unitary_from_matrix():
    circuit = QCircuit()
    circuit << CNOT(q[1], q[0]) << X(q[1])
    return circuit

machine.finalize()
