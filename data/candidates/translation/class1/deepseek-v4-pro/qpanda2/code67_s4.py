# EVAL_META: task_id=67, framework=qpanda2, class=1
import numpy as np
from pyqpanda import *

def chsh_circuit(alice, bob):
    init(QMachineType.CPU)
    q = qAlloc_many(2)
    c = cAlloc_many(2)
    circuit = QCircuit()
    circuit << H(q[0])
    circuit << CNOT(q[0], q[1])
    if alice == 0:
        circuit << RY(q[0], 0.0)
    else:
        circuit << RY(q[0], -np.pi / 2)
    circuit << Measure(q[0], c[0])
    if bob == 0:
        circuit << RY(q[1], -np.pi / 4)
    else:
        circuit << RY(q[1], np.pi / 4)
    circuit << Measure(q[1], c[1])
    return circuit
