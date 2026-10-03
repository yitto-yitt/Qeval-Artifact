# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    for pauli_string, time in zip(pauli_strings, times):
        active_paulis = []
        active_wires = []
        for wire, char in enumerate(reversed(pauli_string)):
            if char != 'I':
                active_paulis.append(char)
                active_wires.append(wire)
        
        if not active_paulis:
            for _ in range(reps):
                qml.GlobalPhase(time / reps)
        else:
            pauli_word = "".join(active_paulis)
            for _ in range(reps):
                qml.PauliRot(2 * time / reps, pauli_word, wires=active_wires)
