# EVAL_META: task_id=60, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, S, Sdag, CNOT

def create_cy_gate():
    q0 = Qubit()
    q1 = Qubit()
    prog = QProg()
    prog << Sdag(q1) << CNOT(q0, q1) << S(q1)
    return prog
