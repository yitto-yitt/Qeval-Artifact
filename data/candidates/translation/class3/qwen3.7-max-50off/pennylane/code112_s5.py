# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])
    wires = list(range(num_wires))
    
    with qml.tape.QuantumTape() as tape:
        for pauli_string, time in zip(pauli_strings, times):
            # Qiskit uses little-endian for Pauli strings, PennyLane uses big-endian
            pl_pauli = pauli_string[::-1]
            for _ in range(reps):
                qml.PauliRot(2 * time / reps, pl_pauli, wires=wires)
                
    return tape
