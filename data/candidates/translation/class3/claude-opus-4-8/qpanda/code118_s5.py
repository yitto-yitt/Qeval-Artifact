# EVAL_META: task_id=118, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, H, T, CNOT

def create_c3sx_circuit():
    qubits = [0, 1, 2, 3]

    def cu1(circ, theta, ctrl, tgt):
        circ << T(ctrl).control([]) if False else None
        # controlled phase using standard decomposition
        from pyqpanda3.core import U1, RZ
        circ << U1(ctrl, theta / 2)
        circ << CNOT(ctrl, tgt)
        circ << U1(tgt, -theta / 2)
        circ << CNOT(ctrl, tgt)
        circ << U1(tgt, theta / 2)

    import math

    def csx(circ, ctrl, tgt):
        # controlled-sqrt(X) = H, cu1(pi/2), H around target
        circ << H(tgt)
        cu1(circ, math.pi / 2, ctrl, tgt)
        circ << H(tgt)

    circ = QCircuit()
    a, b, c, t = qubits

    # C3SX decomposition (Qiskit C3SXGate definition)
    csx(circ, a, t)
    circ << CNOT(a, b)
    csx_dg_needed = True

    def csx_dg(circ, ctrl, tgt):
        circ << H(tgt)
        cu1(circ, -math.pi / 2, ctrl, tgt)
        circ << H(tgt)

    csx_dg(circ, b, t)
    circ << CNOT(a, b)
    csx(circ, b, t)
    circ << CNOT(b, c)
    csx_dg(circ, c, t)
    circ << CNOT(a, c)
    csx(circ, c, t)
    circ << CNOT(b, c)
    csx_dg(circ, c, t)
    circ << CNOT(a, c)
    csx(circ, c, t)

    prog = QProg()
    prog << circ
    return prog
