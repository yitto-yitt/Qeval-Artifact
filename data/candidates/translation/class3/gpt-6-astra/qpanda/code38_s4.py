# EVAL_META: task_id=38, framework=qpanda, class=3
from pyqpanda3.core import CPUQVM, QProg, H, RZ, RY, CNOT


def create_quantum_circuit_based_h0_crz01_h1_cry10(theta):
    prog = QProg()
    prog << H(0)
    prog << RZ(1, theta / 2)
    prog << CNOT(0, 1)
    prog << RZ(1, -theta / 2)
    prog << CNOT(0, 1)
    prog << H(1)
    prog << RY(0, theta / 2)
    prog << CNOT(1, 0)
    prog << RY(0, -theta / 2)
    prog << CNOT(1, 0)

    simulator = CPUQVM()
    simulator.run(prog, 1)
    return prog
