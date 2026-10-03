# EVAL_META: task_id=71, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import CPUQVM, QProg, H, T, RZ, CNOT


def create_quantum_circuit_based_h0_csx01_h1():
    prog = QProg()
    prog << H(2) << H(2)
    prog << H(0)
    prog << H(1)
    prog << T(0) << RZ(1, pi / 4)
    prog << CNOT(0, 1)
    prog << RZ(1, -pi / 4)
    prog << CNOT(0, 1)
    prog << H(1)
    prog << H(1)

    simulator = CPUQVM()
    simulator.run(prog, 1)
    return prog
