# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = qAlloc_many(1)
def circuit():
    qc = QCircuit()
    qc << H(q[0])
    theta = Parameter('th')
    qc << RZ(q[0], theta)
    return qc
machine.finalize()
