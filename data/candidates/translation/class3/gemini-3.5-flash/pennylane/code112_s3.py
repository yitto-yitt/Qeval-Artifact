# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    with qml.tape.QuantumTape() as tape:
        for pauli_string, time in zip(pauli_strings, times):
            active_paulis = []
            active_wires = []
            for i, char in enumerate(pauli_string):
                if char != 'I':
                    active_paulis.append(char)
                    active_wires.append(i)
            
            if not active_paulis:
                continue
            
            pauli_word = "".join(active_paulis)
            theta = 2 * time / reps
            for _ in range(reps):
                qml.PauliRot(theta, pauli_word, wires=active_wires)
    return tape
