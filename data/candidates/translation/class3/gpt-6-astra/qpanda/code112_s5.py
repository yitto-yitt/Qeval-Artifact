# EVAL_META: task_id=112, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, I, H, X, RX, RZ, U1, CNOT


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    if not isinstance(reps, int) or reps < 1:
        raise ValueError("reps must be a positive integer")

    program = QProg()
    for qubit in range(n):
        program << I(qubit)

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) != n or any(p not in "IXYZ" for p in pauli_string):
            raise ValueError("Pauli strings must have equal length and contain only I, X, Y, Z")

        active = [
            (qubit, pauli)
            for qubit, pauli in enumerate(reversed(pauli_string))
            if pauli != "I"
        ]
        step_time = float(time) / reps

        for _ in range(reps):
            if not active:
                program << U1(0, -step_time)
                program << X(0)
                program << U1(0, -step_time)
                program << X(0)
                continue

            for qubit, pauli in active:
                if pauli == "X":
                    program << H(qubit)
                elif pauli == "Y":
                    program << RX(qubit, pi / 2)

            for index in range(len(active) - 1):
                program << CNOT(active[index][0], active[index + 1][0])

            program << RZ(active[-1][0], 2 * step_time)

            for index in reversed(range(len(active) - 1)):
                program << CNOT(active[index][0], active[index + 1][0])

            for qubit, pauli in reversed(active):
                if pauli == "X":
                    program << H(qubit)
                elif pauli == "Y":
                    program << RX(qubit, -pi / 2)

    return program
