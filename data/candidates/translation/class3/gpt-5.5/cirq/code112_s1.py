# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()

    for pauli_string, time in zip(pauli_strings, times):
        active = [(i, p.upper()) for i, p in enumerate(pauli_string) if p.upper() != "I"]

        for _ in range(reps):
            step_time = time / reps

            if not active:
                circuit.append(cirq.global_phase_operation(np.exp(-1j * step_time)))
                continue

            for i, p in active:
                q = qubits[i]
                if p == "X":
                    circuit.append(cirq.H(q))
                elif p == "Y":
                    circuit.append(cirq.S(q) ** -1)
                    circuit.append(cirq.H(q))

            target_index = active[-1][0]
            target = qubits[target_index]

            for i, _ in active[:-1]:
                circuit.append(cirq.CNOT(qubits[i], target))

            circuit.append(cirq.rz(2 * step_time)(target))

            for i, _ in reversed(active[:-1]):
                circuit.append(cirq.CNOT(qubits[i], target))

            for i, p in reversed(active):
                q = qubits[i]
                if p == "X":
                    circuit.append(cirq.H(q))
                elif p == "Y":
                    circuit.append(cirq.H(q))
                    circuit.append(cirq.S(q))

    return circuit
