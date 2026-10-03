# EVAL_META: task_id=44, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(3)

def tensor_circuits():
    circ = QCircuit()
    circ << CRY(q[0], q[1], 0.2)
    circ << X(q[2])
    return circ

machine.finalize()
