# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import QProg, Qubit, H, CRZ, CRY

def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QProg()
    q0 = Qubit(0)
    q1 = Qubit(1)

    prog << H(q0) << CRZ(q0, q1, theta) << H(q1) << CRY(q1, q0, theta)

    return prog
