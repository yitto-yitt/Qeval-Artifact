# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml


def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n)

    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            word = pauli_string[::-1]
            angle = 2.0 * time / reps
            for _ in range(reps):
                qml.PauliRot(angle, word, wires=range(n))
        return qml.state()

    return qml.QNode(circuit, dev)
