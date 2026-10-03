# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    def append_pauli_evolution(pauli_string, theta):
        active = []
        undo_basis = []

        for i, p in enumerate(pauli_string):
            q = qubits[i]
            if p == "X":
                circuit.append(cirq.H(q))
                undo_basis.append(cirq.H(q))
                active.append(q)
            elif p == "Y":
                circuit.append(cirq.S(q) ** -1)
                circuit.append(cirq.H(q))
                undo_basis.append(cirq.H(q))
                undo_basis.append(cirq.S(q))
                active.append(q)
            elif p == "Z":
                active.append(q)
            elif p == "I":
                continue
            else:
                raise ValueError(f"Unsupported Pauli character: {p}")

        if not active:
            circuit.append(cirq.global_phase_operation(np.exp(-1j * theta)))
        else:
            target = active[-1]
            entanglers = [cirq.CNOT(q, target) for q in active[:-1]]
            circuit.append(entanglers)
            circuit.append(cirq.rz(2 * theta)(target))
            circuit.append(reversed(entanglers))

        circuit.append(reversed(undo_basis))

    for pauli_string, time in zip(pauli_strings, times):
        step_time = time / reps
        for _ in range(reps):
            append_pauli_evolution(pauli_string, step_time)

    return circuit
