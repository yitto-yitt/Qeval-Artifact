# EVAL_META: task_id=66, framework=qpanda, class=2
from numpy import arccos, sqrt
from pyqpanda3.core import QCircuit, QProg, RY, H, X, CNOT, measure


def w_state():
    qubits = list(range(3))
    circuit = QCircuit(3)
    circuit << RY(qubits[0], 2 * arccos(1 / sqrt(3)))
    ch = H(qubits[1])
    ch = ch.control([qubits[0]])
    circuit << ch
    circuit << CNOT(qubits[1], qubits[2])
    circuit << CNOT(qubits[0], qubits[1])
    circuit << X(qubits[0])

    prog = QProg()
    prog << circuit
    for q in qubits:
        prog << measure(q, q)
    return prog
