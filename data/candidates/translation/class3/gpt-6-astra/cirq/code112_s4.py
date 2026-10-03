# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    qubits = cirq.LineQubit.range(len(pauli_strings[0]))
    circuit = cirq.Circuit(cirq.I(q) for q in qubits)

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) > len(qubits):
            raise ValueError("Pauli string exceeds the circuit's qubit count.")
        if any(p not in "IXYZ" for p in pauli_string):
            raise ValueError("Pauli strings must contain only I, X, Y, and Z.")

        active = [
            (qubits[i], p)
            for i, p in enumerate(reversed(pauli_string))
            if p != "I"
        ]
        step_time = time / reps

        for _ in range(reps):
            if not active:
                circuit.append(cirq.global_phase_operation(np.exp(-1j * step_time)))
                continue

            basis_changes = []
            for qubit, pauli in active:
                if pauli == "X":
                    basis_changes.append(cirq.H(qubit))
                elif pauli == "Y":
                    basis_changes.extend([cirq.S(qubit) ** -1, cirq.H(qubit)])

            parity = [
                cirq.CNOT(active[i][0], active[i + 1][0])
                for i in range(len(active) - 1)
            ]

            circuit.append(basis_changes)
            circuit.append(parity)
            circuit.append(cirq.rz(2 * step_time)(active[-1][0]))
            circuit.append(cirq.inverse(parity))
            circuit.append(cirq.inverse(basis_changes))

    return circuit
