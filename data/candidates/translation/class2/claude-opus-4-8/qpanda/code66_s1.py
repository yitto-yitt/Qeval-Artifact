# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import QProg, QCircuit, RY, X, CNOT, H, measure


def w_state():
    qubits = list(range(3))
    prog = QProg()

    prog << RY(qubits[0], 2 * arccos(1 / sqrt(3)))

    ch = QCircuit()
    ch << H(qubits[1])
    prog << ch.control([qubits[0]])

    prog << CNOT(qubits[1], qubits[2])
    prog << CNOT(qubits[0], qubits[1])
    prog << X(qubits[0])

    for q in qubits:
        prog << measure(q, q)

    return prog
