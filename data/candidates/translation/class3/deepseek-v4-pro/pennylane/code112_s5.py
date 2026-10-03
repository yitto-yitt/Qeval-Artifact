# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            for _ in range(reps):
                qml.PauliRot(2 * time / reps, pauli_string, wires=range(len(pauli_string)))
        return qml.state()

    return circuit
