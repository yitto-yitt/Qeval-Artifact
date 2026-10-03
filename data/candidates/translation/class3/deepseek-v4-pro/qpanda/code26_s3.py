# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import (
    init,
    QMachineType,
    qAlloc_many,
    cAlloc_many,
    QProg,
    H,
    CNOT,
    Measure,
    QProgToDAG,
)

def bell_dag():
    init(QMachineType.CPU)
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    return QProgToDAG(prog)
