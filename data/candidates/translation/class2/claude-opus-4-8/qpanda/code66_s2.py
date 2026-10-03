# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import QCircuit, QProg, RY, H, X, measure


def w_state():
    qubits = [0, 1, 2]
    circuit = QCircuit()
    circuit << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    circuit << H(qubits[1]).control(qubits[0])
    circuit << X(qubits[2]).control(qubits[1])
    circuit << X(qubits[1]).control(qubits[0])
    circuit << X(qubits[0])

    prog = QProg()
    prog << circuit
    for q in qubits:
        prog << measure(q, q)
    return prog
