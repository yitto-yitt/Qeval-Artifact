# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml


def create_product_formula_circuit(pauli_strings, times, order, reps):
    operations = []
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            operations.append(
                qml.PauliRot(
                    2 * time / reps,
                    pauli_string[::-1],
                    wires=range(len(pauli_string)),
                )
            )
    return qml.tape.QuantumScript(operations)
