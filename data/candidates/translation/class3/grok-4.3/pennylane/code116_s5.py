# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    pauli_op = qml.pauli.string_to_pauli_word(pauli_string)
    evolution_gate = qml.exp(-1j * time * pauli_op)
    return evolution_gate
