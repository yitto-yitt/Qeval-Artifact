# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, CU
import numpy as np


def create_c3sx_circuit():
    qc = QCircuit(4)

    def csx(ctrl, tgt):
        # controlled-sqrt(X) implemented via H and controlled phase rotations
        c = QCircuit(4)
        c << H(tgt)
        c << CU(ctrl, tgt, np.pi / 2, -np.pi / 2, np.pi / 2, 0).control([ctrl]) if False else None
        return c

    def c1sx(ctrl, tgt):
        # Controlled-V (sqrt(X)) = H, controlled-phase(pi/2)-like, H decomposition
        c = QCircuit(4)
        c << H(tgt)
        u = CU(ctrl, tgt, np.pi / 2, 0, 0, 0)
        c << u
        c << H(tgt)
        return c

    # C3SX = 3-controlled sqrt(X). Build via standard decomposition using
    # controlled sqrt(sqrt(...)) is complex; instead use CU with controls.
    # sqrt(X) as a single-qubit unitary: U3(pi/2, -pi/2, pi/2) up to global phase.
    def make_c3sx():
        qc2 = QCircuit(4)
        # Single-qubit sqrt(X) gate matrix parameters for CU(theta,phi,lambda):
        theta, phi, lam = np.pi / 2, -np.pi / 2, np.pi / 2
        base = CU(0, 3, theta, phi, lam, 0)
        controlled = base.control([1, 2])
        qc2 << controlled
        return qc2

    qc = make_c3sx()

    prog = QProg()
    prog << qc
    return prog
