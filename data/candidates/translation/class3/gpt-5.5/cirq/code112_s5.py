# EVAL_META: task_id=112, framework=cirq, class=3
import numpy as np
import cirq

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    repetitions = int(reps)

    for pauli_string, time in zip(pauli_strings, times):
        if len(pauli_string) > num_qubits:
            raise ValueError("Pauli string length exceeds the number of circuit qubits.")

        step_time = time / repetitions
        active = [(i, pauli.upper()) for i, pauli in enumerate(pauli_string) if pauli.upper() != "I"]

        for _ in range(repetitions):
            if not active:
                circuit.append(cirq.global_phase_operation(np.exp(-1j * step_time)))
                continue

            for i, pauli in active:
                q = qubits[i]
                if pauli == "X":
                    circuit.append(cirq.H(q))
                elif pauli == "Y":
                    circuit.append(cirq.S(q) ** -1)
                    circuit.append(cirq.H(q))
                elif pauli == "Z":
                    pass
                else:
                    raise ValueError(f"Unsupported Pauli character: {pauli}")

            target = qubits[active[-1][0]]
            for i, _ in active[:-1]:
                circuit.append(cirq.CNOT(qubits[i], target))

            circuit.append(cirq.rz(rads=2 * step_time).on(target))

            for i, _ in reversed(active[:-1]):
                circuit.append(cirq.CNOT(qubits[i], target))

            for i, pauli in reversed(active):
                q = qubits[i]
                if pauli == "X":
                    circuit.append(cirq.H(q))
                elif pauli == "Y":
                    circuit.append(cirq.H(q))
                    circuit.append(cirq.S(q))

    missing_qubits = [q for q in qubits if q not in circuit.all_qubits()]
    if missing_qubits:
        circuit.append(cirq.I(q) for q in missing_qubits)

    return circuit
