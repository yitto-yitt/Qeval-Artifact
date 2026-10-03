# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, RY, Measure


def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    qc = QProg()
    qc << H(q[0]) << CNOT(q[0], q[1])
    if alice == 0:
        qc << RY(q[0], 0)
    else:
        qc << RY(q[0], -pi / 2)
    qc << Measure(q[0], c[0])
    if bob == 0:
        qc << RY(q[1], -pi / 4)
    else:
        qc << RY(q[1], pi / 4)
    qc << Measure(q[1], c[1])
    return qc
