# EVAL_META: task_id=66, framework=qpanda, class=2
from pyqpanda3.core import CNOT, CZ, CPUQVM, Measure, QProg, RY, X
import numpy as np


def w_state():
    machine = CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)

    prog = QProg()

    # circuit.ry(2 * arccos(1 / sqrt(3)), 0)
    prog << RY(q[0], 2 * np.arccos(1 / np.sqrt(3)))

    # circuit.ch(0, 1) decomposed as RY(q[1], pi/4) -> CZ(q[0], q[1]) -> RY(q[1], -pi/4)
    prog << RY(q[1], np.pi / 4)
    prog << CZ(q[0], q[1])
    prog << RY(q[1], -np.pi / 4)

    # circuit.cx(1, 2)
    prog << CNOT(q[1], q[2])

    # circuit.cx(0, 1)
    prog << CNOT(q[0], q[1])

    # circuit.x(0)
    prog << X(q[0])

    # circuit.measure_all()
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])
    prog << Measure(q[2], c[2])

    return prog
