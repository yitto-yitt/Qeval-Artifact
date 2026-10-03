# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    pauli_word = qml.pauli.string_to_pauli_word(pauli_string)
    hamiltonian = pauli_word.operation(wire_order=list(range(n)))
    evolution = qml.evolve(hamiltonian, time)
    return qml.tape.QuantumScript([evolution], measurements=[])
