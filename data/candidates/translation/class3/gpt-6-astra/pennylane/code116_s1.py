# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml
from scipy.linalg import expm


def synthesize_evolution_gate(pauli_string, time):
    wires = list(range(len(pauli_string)))
    pauli = qml.pauli.string_to_pauli_word(pauli_string)
    matrix = qml.matrix(pauli, wire_order=wires)
    unitary = expm(-1j * time * matrix)
    return qml.tape.QuantumScript(
        [qml.QubitUnitary(unitary, wires=wires)]
    )
