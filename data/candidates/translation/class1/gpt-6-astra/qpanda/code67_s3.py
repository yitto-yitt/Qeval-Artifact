# EVAL_META: task_id=67, framework=qpanda, class=1
from numpy import pi
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, RY, measure


def chsh_circuit(alice, bob):
    prog = QProg()
    prog << H(0)
    prog << CNOT(0, 1)
    prog << RY(0, 0.0 if alice == 0 else -pi / 2)
    prog << measure(0, 0)
    prog << RY(1, -pi / 4 if bob == 0 else pi / 4)
    prog << measure(1, 1)

    qvm = CPUQVM()
    qvm.run(prog, 1)
    return prog
