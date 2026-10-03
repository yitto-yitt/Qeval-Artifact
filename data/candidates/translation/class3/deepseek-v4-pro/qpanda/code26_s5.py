# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

try:
    from pyqpanda3.core import QProgDAG
except ImportError:
    QProgDAG = None


def bell_dag():
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qalloc(3)
    c = qvm.calloc(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    if QProgDAG is not None:
        return QProgDAG(prog)
    return prog
