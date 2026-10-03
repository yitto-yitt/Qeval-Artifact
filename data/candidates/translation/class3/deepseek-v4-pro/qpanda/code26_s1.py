# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import init, QProg, H, CNOT, Measure, qAlloc, cAlloc, qprog_to_dag


def bell_dag():
    machine = init()
    q = qAlloc(machine, 3)
    c = cAlloc(machine, 3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    return qprog_to_dag(prog)
