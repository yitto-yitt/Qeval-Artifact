# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n_qubits)

    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            coeffs = [1.0]
            ops = [qml.pauli.string_to_pauli_word(pauli_string)]
            qml.ApproxTimeEvolution(qml.Hamiltonian(coeffs, ops), time, reps)
        return qml.state()

    circuit.construct([], {})
    return circuit.qtape
