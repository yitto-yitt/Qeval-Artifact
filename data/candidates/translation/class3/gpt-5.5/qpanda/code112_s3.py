# EVAL_META: task_id=112, framework=qpanda, class=3
from math import pi
from pyqpanda3.core import *


def create_product_formula_circuit(pauli_strings, times, order, reps):
    qc = QCircuit()
    if not pauli_strings:
        return qc

    n = len(pauli_strings[0])

    for pauli_string, time in zip(pauli_strings, times):
        active = []

        for idx, p in enumerate(pauli_string):
            qubit = n - 1 - idx
            if p == "I":
                continue
            active.append((qubit, p))
            if p == "X":
                qc << H(qubit)
            elif p == "Y":
                qc << RZ(qubit, -pi / 2)
                qc << H(qubit)

        active_qubits = [q for q, _ in active]

        if len(active_qubits) == 1:
            qc << RZ(active_qubits[0], 2 * time)
        elif len(active_qubits) > 1:
            for i in range(len(active_qubits) - 1):
                qc << CNOT(active_qubits[i], active_qubits[i + 1])

            qc << RZ(active_qubits[-1], 2 * time)

            for i in range(len(active_qubits) - 2, -1, -1):
                qc << CNOT(active_qubits[i], active_qubits[i + 1])

        for qubit, p in reversed(active):
            if p == "X":
                qc << H(qubit)
            elif p == "Y":
                qc << H(qubit)
                qc << RZ(qubit, pi / 2)

    return qc
