# EVAL_META: task_id=67, framework=qpanda2, class=1
from numpy import pi
from pyqpanda import *

def chsh_circuit(alice, bob):
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    circ = QCircuit()
    circ << H(q[0]) << CNOT(q[0], q[1])
    if alice == 0:
        circ << RY(q[0], 0)
    else:
        circ << RY(q[0], -pi / 2)
    circ << Measure(q[0], c[0])
    if bob == 0:
        circ << RY(q[1], -pi / 4)
    else:
        circ << RY(q[1], pi / 4)
    circ << Measure(q[1], c[1])
    return circ
