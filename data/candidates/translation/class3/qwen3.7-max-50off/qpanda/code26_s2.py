# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, Cbit, H, CNOT, Measure

def bell_dag():
    q = [Qubit(i) for i in range(3)]
    c = [Cbit(i) for i in range(3)]
    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    return prog
