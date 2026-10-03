# EVAL_META: task_id=26, framework=qpanda, class=3
from pyqpanda3.core import init_qvm, qAlloc_many, cAlloc_many, QProg, H, CNOT, Measure, qprog_to_dag


def bell_dag():
    init_qvm()
    q = qAlloc_many(3)
    c = cAlloc_many(3)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0])
    dag = qprog_to_dag(prog)
    return dag
