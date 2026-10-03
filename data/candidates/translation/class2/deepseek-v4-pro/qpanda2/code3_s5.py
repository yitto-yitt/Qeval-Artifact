# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import *


def create_ghz(drawing=False):
    if not hasattr(create_ghz, "_init"):
        init(QMachineType.CPU)
        create_ghz._init = True

    q = qAlloc_many(3)
    c = cAlloc_many(3)

    ghz = QCircuit()
    ghz << H(q[0])
    ghz << CNOT(q[0], q[1])
    ghz << CNOT(q[0], q[2])
    for i in range(3):
        ghz << Measure(q[i], c[i])

    if drawing:
        prog = QProg()
        prog << ghz
        return ghz, draw_qprog(prog)

    return ghz
