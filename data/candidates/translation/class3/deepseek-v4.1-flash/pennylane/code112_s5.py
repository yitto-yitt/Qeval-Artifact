# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_wires = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n_wires)
    
    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            obs = qml.pauli.string_to_pauli_word(pauli_string)
            qml.exp(obs, -1j * time)
        return qml.state()
    return circuit
