# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, T, X, RZ
import numpy as np


def create_c3sx_circuit():
    qubits = list(range(4))
    a, b, c, d = qubits

    def csx(ctrl, tgt):
        circ = QCircuit()
        circ << H(tgt)
        circ << (RZ(tgt, np.pi / 4)).control(ctrl)
        circ << H(tgt)
        return circ

    qc = QCircuit()
    qc << H(d)
    qc << (RZ(d, np.pi / 4)).control(a)
    qc << H(d)

    qc << X(b).control(a)
    qc << H(d)
    qc << (RZ(d, -np.pi / 4)).control(b)
    qc << H(d)
    qc << X(b).control(a)

    qc << H(d)
    qc << (RZ(d, np.pi / 4)).control(b)
    qc << H(d)

    qc << X(c).control(b)
    qc << H(d)
    qc << (RZ(d, -np.pi / 4)).control(c)
    qc << H(d)
    qc << X(c).control(a)
    qc << H(d)
    qc << (RZ(d, np.pi / 4)).control(c)
    qc << H(d)
    qc << X(c).control(b)
    qc << H(d)
    qc << (RZ(d, -np.pi / 4)).control(c)
    qc << H(d)
    qc << X(c).control(a)

    qc << H(d)
    qc << (RZ(d, np.pi / 4)).control(c)
    qc << H(d)

    prog = QProg()
    prog << qc
    return prog
