# EVAL_META: task_id=41, framework=cirq, class=3
import numpy as np
import cirq


def compose_op():
    num_qubits = 3
    pauli_label = "YX"
    qargs = [0, 2]

    matrices = {
        "I": np.eye(2, dtype=complex),
        "X": cirq.unitary(cirq.X),
        "Y": cirq.unitary(cirq.Y),
        "Z": cirq.unitary(cirq.Z),
    }

    labels_by_qubit = ["I"] * num_qubits
    for local_qubit, global_qubit in enumerate(qargs):
        labels_by_qubit[global_qubit] = pauli_label[-1 - local_qubit]

    embedded = matrices[labels_by_qubit[-1]]
    for label in reversed(labels_by_qubit[:-1]):
        embedded = np.kron(embedded, matrices[label])

    op = np.eye(2**num_qubits, dtype=complex)
    return cirq.MatrixGate(embedded @ op)
