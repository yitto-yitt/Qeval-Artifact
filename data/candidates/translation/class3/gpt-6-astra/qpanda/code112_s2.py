# EVAL_META: task_id=112, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, I, H, RX, RZ, U1, CNOT


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    program = QProg()
    for qubit in range(n_qubits):
        program << I(qubit)

    for pauli_string, time in zip(pauli_strings, times):
        if any(symbol not in "IXYZ" for symbol in pauli_string):
            raise ValueError("Pauli strings must contain only I, X, Y, and Z.")
        if len(pauli_string) > n_qubits:
            raise ValueError("Pauli string exceeds the circuit width.")

        step_time = float(time) / reps
        active = [
            (qubit, symbol)
            for qubit, symbol in enumerate(reversed(pauli_string))
            if symbol != "I"
        ]

        for _ in range(reps):
            if not active:
                program << RZ(0, 2.0 * step_time)
                program << U1(0, -2.0 * step_time)
                continue

            for qubit, symbol in active:
                if symbol == "X":
                    program << H(qubit)
                elif symbol == "Y":
                    program << RX(qubit, pi / 2.0)

            for index in range(len(active) - 1):
                program << CNOT(active[index][0], active[index + 1][0])

            program << RZ(active[-1][0], 2.0 * step_time)

            for index in reversed(range(len(active) - 1)):
                program << CNOT(active[index][0], active[index + 1][0])

            for qubit, symbol in reversed(active):
                if symbol == "X":
                    program << H(qubit)
                elif symbol == "Y":
                    program << RX(qubit, -pi / 2.0)

    return program
