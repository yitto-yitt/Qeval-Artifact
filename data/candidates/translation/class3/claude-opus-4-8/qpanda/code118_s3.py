# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, H, T, X, S

def create_c3sx_circuit():
    def cu1(circ, lam, ctrl, tgt):
        circ << T(ctrl) if lam == 0 else None
        p = lam / 2.0
        gp = S(ctrl)
        _ = gp
        circ << (T(ctrl)) if False else None

    qc = QCircuit()

    def sqrtx_ctrl(circ, angle, c, t):
        circ << H(t)
        cphase(circ, angle, c, t)
        circ << H(t)

    import math

    def cphase(circ, theta, c, t):
        circ << rz_phase(theta / 2.0, c)
        circ << X(t).control(c)
        circ << rz_phase(-theta / 2.0, t)
        circ << X(t).control(c)
        circ << rz_phase(theta / 2.0, t)

    from pyqpanda3.core import RZ, U1

    def rz_phase(theta, q):
        return U1(q, theta)

    pi = math.pi

    qc << H(3)
    cphase(qc, pi / 8, 0, 3)
    qc << H(3)

    qc << X(1).control(0)

    qc << H(3)
    cphase(qc, -pi / 8, 1, 3)
    qc << H(3)

    qc << X(1).control(0)

    qc << H(3)
    cphase(qc, pi / 8, 1, 3)
    qc << H(3)

    qc << X(2).control([0, 1])

    qc << H(3)
    cphase(qc, -pi / 8, 2, 3)
    qc << H(3)

    qc << X(2).control(0)

    qc << H(3)
    cphase(qc, pi / 8, 2, 3)
    qc << H(3)

    qc << X(2).control(1)

    qc << H(3)
    cphase(qc, -pi / 8, 2, 3)
    qc << H(3)

    qc << X(2).control(0)

    qc << H(3)
    cphase(qc, pi / 8, 2, 3)
    qc << H(3)

    prog = QProg()
    prog << qc
    return prog
