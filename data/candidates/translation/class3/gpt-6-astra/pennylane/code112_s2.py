# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    operations = [qml.Identity(wires=wire) for wire in range(num_qubits)]

    for pauli_string, time in zip(pauli_strings, times):
        angle = 2 * time / reps
        for _ in range(reps):
            operations.append(
                qml.PauliRot(
                    angle,
                    pauli_string[::-1],
                    wires=range(len(pauli_string)),
                )
            )

    return qml.tape.QuantumScript(operations)
