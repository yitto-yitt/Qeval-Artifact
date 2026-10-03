# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)

    ghz = QProg()
    ghz << H(q[0])
    ghz << CNOT(q[0], q[1])
    ghz << CNOT(q[0], q[2])
    ghz << Measure(q[0], c[0])
    ghz << Measure(q[1], c[1])
    ghz << Measure(q[2], c[2])

    ghz._qvm = qvm

    if drawing:
        return ghz, draw_qprog(ghz, "text")
    return ghz
