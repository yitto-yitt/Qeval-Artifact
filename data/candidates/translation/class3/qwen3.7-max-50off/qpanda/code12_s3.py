# EVAL_META: task_id=12, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QProg, H, CNOT, get_matrix

def get_unitary():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    return get_matrix(prog)
