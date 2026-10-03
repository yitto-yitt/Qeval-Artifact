# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QuantumProgram, C3SX

def create_c3sx_circuit():
    qprog = QuantumProgram()
    q = qprog.qAlloc_many(4)
    c3sx = C3SX(q[0], q[1], q[2], q[3])
    qprog << c3sx
    return qprog
