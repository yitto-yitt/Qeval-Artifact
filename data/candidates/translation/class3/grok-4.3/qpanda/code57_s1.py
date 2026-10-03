# EVAL_META: task_id=57, framework=qpanda, class=3
from pyqpanda3.core import QProg, CNOT, qAlloc_many

def create_swap_gate():
    qprog = QProg()
    q = qAlloc_many(2)
    qprog << CNOT(q[0], q[1]) << CNOT(q[1], q[0]) << CNOT(q[0], q[1])
    return qprog
