# EVAL_META: task_id=67, framework=qpanda, class=1
from math import pi
from pyqpanda3.core import CPUQVM, QCircuit, H, CNOT, BARRIER, RY, Measure


def chsh_circuit(alice, bob):
    qvm = CPUQVM()
    qvm.init()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    circ = QCircuit()
    circ << H(qubits[0]) \
         << CNOT(qubits[0], qubits[1]) \
         << BARRIER(qubits)
    if alice == 0:
        circ << RY(qubits[0], 0.0)
    else:
        circ << RY(qubits[0], -pi / 2)
    circ << Measure(qubits[0], cbits[0])
    if bob == 0:
        circ << RY(qubits[1], -pi / 4)
    else:
        circ << RY(qubits[1], pi / 4)
    circ << Measure(qubits[1], cbits[1])
    return circ
