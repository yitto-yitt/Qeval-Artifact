# EVAL_META: task_id=90, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(4)
def create_custom_controlled():
    custom = QCircuit()
    custom << X(q[1]) << H(q[2])
    controlled = custom.control([q[0], q[3]])
    circ = QCircuit()
    circ << controlled
    return circ
machine.finalize()
