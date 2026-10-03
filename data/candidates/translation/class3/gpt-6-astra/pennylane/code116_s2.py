# EVAL_META: task_id=116, framework=pennylane, class=3
import numpy as np
import pennylane as qml
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    matrices = {
        "I": np.eye(2, dtype=complex),
        "X": np.array([[0, 1], [1, 0]], dtype=complex),
        "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
        "Z": np.array([[1, 0], [0, -1]], dtype=complex),
    }

    hamiltonian = np.ones((1, 1), dtype=complex)
    for symbol in pauli_string:
        hamiltonian = np.kron(hamiltonian, matrices[symbol])

    with qml.queuing.AnnotatedQueue() as queue:
        if pauli_string:
            qml.QubitUnitary(
                expm(-1j * time * hamiltonian),
                wires=range(len(pauli_string)),
            )
        else:
            qml.GlobalPhase(time)

    return qml.tape.QuantumScript.from_queue(queue)
