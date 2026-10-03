# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
from pyqpanda import QuantumCircuit


def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    if alice == 0:
        qc.ry(0, 0)
    else:
        qc.ry(0, -pi / 2)
    qc.measure(0, 0)
    if bob == 0:
        qc.ry(1, -pi / 4)
    else:
        qc.ry(1, pi / 4)
    qc.measure(1, 1)
    return qc
