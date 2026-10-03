# EVAL_META: task_id=116, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, I, H, RX, RZ, U1, CNOT


def synthesize_evolution_gate(pauli_string, time):
    if not isinstance(pauli_string, str) or not pauli_string:
        raise ValueError("pauli_string must be a nonempty Pauli string.")
    if any(p not in "IXYZ" for p in pauli_string):
        raise ValueError("pauli_string may contain only I, X, Y, and Z.")

    time = float(time)
    program = QProg()
    paulis = list(reversed(pauli_string))

    for qubit in range(len(paulis)):
        program << I(qubit)

    active = [qubit for qubit, pauli in enumerate(paulis) if pauli != "I"]

    if not active:
        program << RZ(0, 2.0 * time)
        program << U1(0, -2.0 * time)
        return program

    for qubit in active:
        if paulis[qubit] == "X":
            program << H(qubit)
        elif paulis[qubit] == "Y":
            program << RX(qubit, pi / 2.0)

    target = active[-1]
    for control in active[:-1]:
        program << CNOT(control, target)

    program << RZ(target, 2.0 * time)

    for control in reversed(active[:-1]):
        program << CNOT(control, target)

    for qubit in reversed(active):
        if paulis[qubit] == "X":
            program << H(qubit)
        elif paulis[qubit] == "Y":
            program << RX(qubit, -pi / 2.0)

    return program
