# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, RX


def rx_gate(value=None):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    prog = QProg()
    theta = 0.0 if value is None else float(value)
    prog.insert(RX(q[0], theta))
    qvm.finalize()
    return prog
