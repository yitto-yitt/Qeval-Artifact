# EVAL_META: task_id=112, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, RX, RY, RZ, H, CNOT
import numpy as np


def _basis_change(circ, qubit, pauli, dagger=False):
    if pauli == 'X':
        circ << H(qubit)
    elif pauli == 'Y':
        if dagger:
            circ << RX(qubit, -np.pi / 2)
        else:
            circ << RX(qubit, np.pi / 2)


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    circ = QCircuit()

    for pauli_string, time in zip(pauli_strings, times):
        # Qiskit Pauli string is little-endian: leftmost char = highest qubit index
        pauli = pauli_string[::-1]

        active = [i for i, p in enumerate(pauli) if p != 'I']

        angle = 2.0 * time / reps

        for _ in range(reps):
            if not active:
                continue

            # Basis change
            for i in active:
                _basis_change(circ, i, pauli[i], dagger=False)

            # CNOT ladder
            for k in range(len(active) - 1):
                circ << CNOT(active[k], active[k + 1])

            # RZ rotation on the last active qubit
            circ << RZ(active[-1], angle)

            # Reverse CNOT ladder
            for k in range(len(active) - 2, -1, -1):
                circ << CNOT(active[k], active[k + 1])

            # Undo basis change
            for i in active:
                _basis_change(circ, i, pauli[i], dagger=True)

    prog = QProg()
    prog << circ
    return prog
