# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])

    pauli_map = {'I': qml.Identity, 'X': qml.PauliX, 'Y': qml.PauliY, 'Z': qml.PauliZ}

    def build_pauli_op(pauli_string):
        op = None
        for i, p in enumerate(pauli_string):
            term = pauli_map[p](i)
            op = term if op is None else op @ term
        return op

    dev = qml.device("default.qubit", wires=num_wires)

    @qml.qnode(dev)
    def circuit():
        for pauli_string, time in zip(pauli_strings, times):
            op = build_pauli_op(pauli_string)
            for _ in range(reps):
                qml.exp(op, -1j * time / reps)
        return qml.state()

    return circuit
