# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml


def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])
    with qml.tape.QuantumTape() as circuit:
        for pauli_string, time in zip(pauli_strings, times):
            for _ in range(reps):
                qml.PauliRot(
                    2 * time / reps,
                    pauli_string[::-1],
                    wires=range(len(pauli_string)),
                )
        for wire in range(num_wires):
            qml.Identity(wires=wire)
    return circuit
