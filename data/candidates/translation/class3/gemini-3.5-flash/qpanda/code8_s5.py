# EVAL_META: task_id=8, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, RX, Var

def rx_gate(value=None):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubit = qvm.qAlloc()
    prog = QProg()
    if value is not None:
        theta = Var(float(value))
    else:
        theta = Var(0.0)
    prog << RX(qubit, theta)
    return prog
