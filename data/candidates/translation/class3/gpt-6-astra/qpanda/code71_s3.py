# EVAL_META: task_id=71, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, S, I


def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << I(2)
    prog << H(0)
    prog << H(1)
    prog << S(1).control([0])
    prog << H(1)
    prog << H(1)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
