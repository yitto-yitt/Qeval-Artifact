# EVAL_META: task_id=5, framework=qpanda, class=2
from pyqpanda3.core import QuantumMachine, QProg, X


def create_state_prep():
    machine = QuantumMachine()
    q = machine.qAlloc_many(2)
    prog = QProg()
    prog << X(q[0])
    return prog
