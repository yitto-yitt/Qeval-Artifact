# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, CNOT, Measure, Qubit, Cbit

def bell_dag():
    q = [Qubit() for _ in range(3)]
    c = [Cbit() for _ in range(3)]
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    return prog
