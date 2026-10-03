# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    ops = []
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            ops.append(qml.PauliRot(2 * time, pauli_string, wires=range(num_qubits)))
    return qml.tape.QuantumScript(ops)
