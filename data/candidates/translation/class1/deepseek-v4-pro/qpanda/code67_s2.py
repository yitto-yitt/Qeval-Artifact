# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import QuantumCircuit


def chsh_circuit(alice, bob):
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    if alice == 0:
        qc.ry(0.0, 0)
    else:
        qc.ry(-pi / 2.0, 0)
    qc.measure(0, 0)
    if bob == 0:
        qc.ry(-pi / 4.0, 1)
    else:
        qc.ry(pi / 4.0, 1)
    qc.measure(1, 1)
    return qc
