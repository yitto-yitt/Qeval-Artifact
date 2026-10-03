# EVAL_META: task_id=3, framework=qpanda, class=2
from pyqpanda3.core import CPUQVM, QCircuit, QProg, H, CNOT, Measure


def create_ghz(drawing=False):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    ghz = QCircuit()
    ghz << H(q[0]) << CNOT(q[0], q[1]) << CNOT(q[0], q[2])
    prog = QProg()
    prog << ghz
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1]) << Measure(q[2], c[2])
    if drawing:
        return prog, None
    return prog
