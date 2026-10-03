# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import QProg, RY, CH, CNOT, X, Measure, Qubit, CBit


def w_state():
    prog = QProg()
    qubits = [Qubit(i) for i in range(3)]
    cbits = [CBit(i) for i in range(3)]

    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    prog << CH(qubits[0], qubits[1])
    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])

    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])
    prog << Measure(qubits[2], cbits[2])

    return prog
