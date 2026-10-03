# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    with qml.tape.QuantumTape() as circuit:
        for pauli_string, time in zip(pauli_strings, times):
            angle = 2 * time / reps
            for _ in range(reps):
                qml.PauliRot(
                    angle,
                    pauli_string[::-1],
                    wires=range(len(pauli_string)),
                )
    return circuit
