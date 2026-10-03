# EVAL_META: task_id=27, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(3)


def apply_op_back():
    circ = QCircuit()
    circ << H(q[0])
    circ << CNOT(q[0], q[1])
    circ << H(q[0])
    return circ


machine.finalize()
