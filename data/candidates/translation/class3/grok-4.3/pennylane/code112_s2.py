# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n_qubits = len(pauli_strings[0])
    with qml.tape.QuantumTape() as tape:
        for pauli_string, time in zip(pauli_strings, times):
            qml.PauliRot(2 * time, pauli_string, wires=range(n_qubits))
    return tape
