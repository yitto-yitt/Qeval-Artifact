# EVAL_META: task_id=112, framework=cirq, class=3
import cirq
import numpy as np
from cirq import PauliString, Circuit, Moment, ops

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        raise ValueError("pauli_strings must not be empty")
    num_qubits = len(pauli_strings[0])
    qubits = cirq.LineQubit.range(num_qubits)

    def pauli_from_string(label, q):
        if label == 'I':
            return cirq.I(q)
        elif label == 'X':
            return cirq.X(q)
        elif label == 'Y':
            return cirq.Y(q)
        elif label == 'Z':
            return cirq.Z(q)
        else:
            raise ValueError(f"Invalid Pauli label: {label}")

    def apply_pauli_string(circuit, pauli_str, time):
        ops_list = []
        for i, ch in enumerate(pauli_str):
            if ch != 'I':
                ops_list.append(pauli_from_string(ch, qubits[i]))
        if not ops_list:
            return
        if len(ops_list) == 1:
            unitary = np.cos(time) * np.eye(2) - 1j * np.sin(time) * cirq.unitary(ops_list[0])
            circuit.append(cirq.MatrixGate(unitary).on(*[q for op in ops_list for q in op.qubits]))
        else:
            cliff = cirq.Circuit()
            cliff.append([op for op in ops_list])
            exp_z = cirq.Circuit()
            exp_z.append(cirq.rz(2 * time).on(qubits[-1]))
            if len(ops_list) > 1:
                change_of_basis = cirq.Circuit()
                target = qubits[-1]
                for op in ops_list[:-1]:
                    if op.gate == cirq.X:
                        change_of_basis.append(cirq.H(op.qubits[0]))
                        change_of_basis.append(cirq.CNOT(op.qubits[0], target))
                        change_of_basis.append(cirq.H(op.qubits[0]))
                    elif op.gate == cirq.Y:
                        change_of_basis.append(cirq.rx(-np.pi/2).on(op.qubits[0]))
                        change_of_basis.append(cirq.CNOT(op.qubits[0], target))
                        change_of_basis.append(cirq.rx(np.pi/2).on(op.qubits[0]))
                if change_of_basis:
                    circuit.append(change_of_basis)
                circuit.append(cirq.CNOT(ops_list[0].qubits[0], target))
            circuit.append(exp_z)
            if len(ops_list) > 1:
                circuit.append(cirq.CNOT(ops_list[0].qubits[0], target))
                if change_of_basis:
                    circuit.append(cirq.inverse(change_of_basis))

    full_circuit = Circuit()
    for pauli_string, time in zip(pauli_strings, times):
        evo_circuit = Circuit()
        for _ in range(reps):
            apply_pauli_string(evo_circuit, pauli_string, time / reps)
        full_circuit += evo_circuit

    return full_circuit
