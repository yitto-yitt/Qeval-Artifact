# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    op = np.eye(2**3, dtype=complex)
    pauli_label = "YX"
    qargs = [0, 2]
    num_qubits = 3

    full_label = ["I"] * num_qubits
    for other_qubit, target_qubit in enumerate(qargs):
        full_label[num_qubits - 1 - target_qubit] = pauli_label[len(pauli_label) - 1 - other_qubit]

    embedded = cirq.unitary(cirq.DensePauliString("".join(full_label)))
    return cirq.MatrixGate(embedded @ op)
