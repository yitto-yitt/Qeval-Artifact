# EVAL_META: task_id=3, framework=qpanda2, class=2
from pyqpanda import init, QMachineType, qAlloc_many, cAlloc_many, QProg, H, CNOT, Measure, draw_qprog


def create_ghz(drawing=False):
    init(QMachineType.CPU)

    q = qAlloc_many(3)
    c = cAlloc_many(3)

    ghz = QProg()
    ghz << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    for i in range(3):
        ghz << Measure(q[i], c[i])

    if drawing:
        return ghz, draw_qprog(ghz, output="mpl")
    return ghz
