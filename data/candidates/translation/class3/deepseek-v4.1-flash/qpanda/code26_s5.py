# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Measure, Qubit, CBit

def bell_dag():
    q = [Qubit(i) for i in range(3)]
    c = [CBit(i) for i in range(3)]
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    return prog
