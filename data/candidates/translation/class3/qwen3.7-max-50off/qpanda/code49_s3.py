# EVAL_META: task_id=49, framework=qpanda, class=3
from pyqpanda3.core import QuantumMachine, QProg, H, CNOT

def simple_elitzur_vaidman():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << H(q[0])
    return prog
