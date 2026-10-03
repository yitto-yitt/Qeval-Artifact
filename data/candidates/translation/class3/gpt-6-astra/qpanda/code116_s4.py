# EVAL_META: task_id=116, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import QProg, I, H, RX, RZ, U1, CNOT


def synthesize_evolution_gate(pauli_string, time):
    label = pauli_string
    sign = 1
    if label.startswith("-"):
        sign = -1
        label = label[1:]
    elif label.startswith("+"):
        label = label[1:]

    if not label or any(p not in "IXYZ" for p in label):
        raise ValueError("Expected a nonempty Hermitian Pauli string.")

    angle = 2.0 * sign * float(time)
    program = QProg()

    for qubit in range(len(label)):
        program << I(qubit)

    active = [
        (qubit, pauli)
        for qubit, pauli in enumerate(reversed(label))
        if pauli != "I"
    ]

    if not active:
        program << RZ(0, angle)
        program << U1(0, -angle)
        return program

    for qubit, pauli in active:
        if pauli == "X":
            program << H(qubit)
        elif pauli == "Y":
            program << RX(qubit, np.pi / 2.0)

    target = active[-1][0]
    for qubit, _ in active[:-1]:
        program << CNOT(qubit, target)

    program << RZ(target, angle)

    for qubit, _ in reversed(active[:-1]):
        program << CNOT(qubit, target)

    for qubit, pauli in reversed(active):
        if pauli == "X":
            program << H(qubit)
        elif pauli == "Y":
            program << RX(qubit, -np.pi / 2.0)

    return program
