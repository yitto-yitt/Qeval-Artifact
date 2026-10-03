# EVAL_META: task_id=112, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import QProg, I, H, X, RX, RZ, U3, CNOT


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    program = QProg()
    for qubit in range(n_qubits):
        program << I(qubit)

    for pauli_string, time in zip(pauli_strings, times):
        active = [
            (qubit, axis)
            for qubit, axis in enumerate(reversed(pauli_string))
            if axis != "I"
        ]
        step_time = float(time) / reps

        for _ in range(reps):
            if not active:
                program << U3(0, 0.0, 0.0, -step_time)
                program << X(0)
                program << U3(0, 0.0, 0.0, -step_time)
                program << X(0)
                continue

            for qubit, axis in active:
                if axis == "X":
                    program << H(qubit)
                elif axis == "Y":
                    program << RX(qubit, pi / 2)

            for index in range(len(active) - 1):
                program << CNOT(active[index][0], active[index + 1][0])

            program << RZ(active[-1][0], 2.0 * step_time)

            for index in reversed(range(len(active) - 1)):
                program << CNOT(active[index][0], active[index + 1][0])

            for qubit, axis in reversed(active):
                if axis == "X":
                    program << H(qubit)
                elif axis == "Y":
                    program << RX(qubit, -pi / 2)

    return program
