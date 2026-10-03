# EVAL_META: task_id=109, framework=qpanda2, class=3
from pyqpanda import *
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(1)
def circuit():
    qc = QCircuit()
    qc << H(q[0])
    qc << RZ(q[0], "th")
    return qc
machine.finalize()
