# EVAL_META: task_id=10, framework=qpanda, class=3
from pyqpanda3.core import QProg, QuantumMachine, X

def create_operator():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = QProg()
    prog.insert(X(q[0]))
    prog.insert(X(q[1]))
    return prog
