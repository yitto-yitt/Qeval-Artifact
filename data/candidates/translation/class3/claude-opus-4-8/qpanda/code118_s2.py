# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, X, T, RZ
import numpy as np


def create_c3sx_circuit():
    qubits = [0, 1, 2, 3]

    def csx(ctrl, tgt):
        c = QCircuit()
        c << H(tgt)
        c << (RZ(tgt, np.pi / 4).control([ctrl]))
        c << (RZ(ctrl, np.pi / 4))
        c << H(tgt)
        return c

    circ = QCircuit()
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[0]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], -np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[1]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[0]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], -np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[2]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[0]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], -np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[1]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[0]]))
    circ << H(qubits[3])
    circ << (RZ(qubits[3], -np.pi / 8))
    circ << H(qubits[3])
    circ << (X(qubits[3]).control([qubits[2]]))
    circ << H(qubits[3])

    prog = QProg()
    prog << circ
    return prog
