# EVAL_META: task_id=105, framework=qpanda, class=3
from pyqpanda3.core import QProg, QuantumMachine, CNOT, T

def initialize_cnot_dihedral():
    qm = QuantumMachine()
    q = qm.qAlloc_many(2)
    prog = QProg()
    prog << CNOT(q[0], q[1])
    prog << T(q[0])
    return prog
