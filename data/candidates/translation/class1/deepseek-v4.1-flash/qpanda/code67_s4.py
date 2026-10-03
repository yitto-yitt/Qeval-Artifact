# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import QCircuit, H, CNOT, RY, Measure, Qubit, CBit

def chsh_circuit(alice, bob):
    qc = QCircuit()
    q0 = Qubit(0)
    q1 = Qubit(1)
    c0 = CBit(0)
    c1 = CBit(1)

    qc << H(q0)
    qc << CNOT(q0, q1)

    if alice == 0:
        qc << RY(q0, 0)
    else:
        qc << RY(q0, -pi / 2)
    qc << Measure(q0, c0)

    if bob == 0:
        qc << RY(q1, -pi / 4)
    else:
        qc << RY(q1, pi / 4)
    qc << Measure(q1, c1)

    return qc
