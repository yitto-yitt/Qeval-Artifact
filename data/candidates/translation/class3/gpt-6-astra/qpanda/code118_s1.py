# EVAL_META: task_id=118, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, H, CNOT, U3


def create_c3sx_circuit():
    prog = QProg()
    prog << H(3)

    for mask in range(1, 16):
        qubits = [q for q in range(4) if mask & (1 << q)]
        target = qubits[-1]
        controls = qubits[:-1]

        for control in controls:
            prog << CNOT(control, target)

        angle = (pi / 16) * (-1 if len(qubits) % 2 == 0 else 1)
        prog << U3(target, 0.0, 0.0, angle)

        for control in reversed(controls):
            prog << CNOT(control, target)

    prog << H(3)
    return prog
