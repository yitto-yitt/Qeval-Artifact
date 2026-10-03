# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(n)
    circuit = cirq.Circuit()
    circuit.append([cirq.I(q) for q in qubits])

    def _parse_pauli_label(label):
        label = str(label).strip()
        coeff = 1
        lower = label.lower()
        if lower.startswith("-i"):
            coeff = -1j
            label = label[2:]
        elif lower.startswith("+i"):
            coeff = 1j
            label = label[2:]
        elif lower.startswith("i"):
            coeff = 1j
            label = label[1:]
        elif label.startswith("-"):
            coeff = -1
            label = label[1:]
        elif label.startswith("+"):
            coeff = 1
            label = label[1:]
        return coeff, label.upper()

    for pauli_string, time in zip(pauli_strings, times):
        coeff, label = _parse_pauli_label(pauli_string)
        if coeff not in (1, -1):
            raise ValueError("PauliEvolutionGate requires a Hermitian Pauli operator.")

        step_time = coeff * time / reps
        active = [(i, p) for i, p in enumerate(label) if p != "I"]

        for _ in range(reps):
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
                elif p != "Z":
                    raise ValueError(f"Invalid Pauli character: {p}")

            target = qubits[active[-1][0]]
            for i, _ in active[:-1]:
                circuit.append(cirq.CNOT(qubits[i], target))

            circuit.append(cirq.rz(2 * step_time).on(target))

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
