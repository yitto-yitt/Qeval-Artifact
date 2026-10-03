# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])
    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def circuit():
        for _ in range(reps):
            for pauli_string, t in zip(pauli_strings, times):
                qml.PauliRot(2.0 * t / reps, pauli_string, wires=list(range(num_wires)))
        return qml.state()

    return circuit.qtape
