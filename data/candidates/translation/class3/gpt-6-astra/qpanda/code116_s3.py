# EVAL_META: task_id=116, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, I, H, X, RX, RZ, U1, CNOT


def synthesize_evolution_gate(pauli_string, time):
    if not pauli_string or any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string must be a nonempty string of I, X, Y, and Z.")

    program = QProg()
    paulis = list(reversed(pauli_string))
    active = [q for q, p in enumerate(paulis) if p != "I"]
    angle = float(time)

    for q in range(len(paulis)):
        program << I(q)

    if not active:
        program << U1(0, -angle) << X(0)
        program << U1(0, -angle) << X(0)
        return program

    for q in active:
        if paulis[q] == "X":
            program << H(q)
        elif paulis[q] == "Y":
            program << RX(q, pi / 2)

    for control, target in zip(active[:-1], active[1:]):
        program << CNOT(control, target)

    program << RZ(active[-1], 2 * angle)

    for control, target in reversed(list(zip(active[:-1], active[1:]))):
        program << CNOT(control, target)

    for q in reversed(active):
        if paulis[q] == "X":
            program << H(q)
        elif paulis[q] == "Y":
            program << RX(q, -pi / 2)

    return program
