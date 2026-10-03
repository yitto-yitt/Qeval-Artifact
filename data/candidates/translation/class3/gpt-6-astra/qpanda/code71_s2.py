# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import QProg, H, T, CNOT, I

def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << I(2)
    prog << H(0)

    # Controlled-SX = H(target) controlled-S H(target).
    prog << H(1)
    prog << T(0) << T(1) << CNOT(0, 1)
    for _ in range(7):
        prog << T(1)
    prog << CNOT(0, 1)
    prog << H(1)

    prog << H(1)
    return prog
