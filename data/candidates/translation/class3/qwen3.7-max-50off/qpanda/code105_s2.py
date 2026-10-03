# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, CNOT, T

def initialize_cnot_dihedral():
    q0 = Qubit()
    q1 = Qubit()
    prog = QProg()
    prog << CNOT(q0, q1)
    prog << T(q0)
    return prog
