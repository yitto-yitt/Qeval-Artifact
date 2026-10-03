# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    q0 = Qubit(0)
    q1 = Qubit(1)
    q2 = Qubit(2)
    c0 = CBit(0)
    c1 = CBit(1)
    c2 = CBit(2)

    ghz = QProg()
    ghz << H(q0)
    ghz << CNOT(q0, q1)
    ghz << CNOT(q0, q2)
    ghz << Measure(q0, c0)
    ghz << Measure(q1, c1)
    ghz << Measure(q2, c2)

    if drawing:
        return ghz, draw_qprog(ghz, 'text')
    return ghz
