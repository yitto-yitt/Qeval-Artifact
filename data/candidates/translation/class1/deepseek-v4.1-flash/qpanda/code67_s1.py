# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, RY, Measure, BARRIER


def chsh_circuit(alice, bob):
    q = [Qubit(0), Qubit(1)]
    c = [CBit(0), CBit(1)]
    qc = QCircuit()
    qc << H(q[0])
    qc << CNOT(q[0], q[1])
    qc << BARRIER([q[0], q[1]])
    if alice == 0:
        qc << RY(q[0], 0.0)
    else:
        qc << RY(q[0], -pi / 2)
    qc << Measure(q[0], c[0])
    if bob == 0:
        qc << RY(q[1], -pi / 4)
    else:
        qc << RY(q[1], pi / 4)
    qc << Measure(q[1], c[1])
    return qc
