# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml
from pennylane.pauli import string_to_pauli_word

def create_product_formula_circuit(pauli_strings, times, order, reps):
    wires = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=wires)

    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            word = string_to_pauli_word(pauli_string)
            for _ in range(reps):
                qml.exp(word, -1j * time / reps)
        return qml.state()

    return circuit
