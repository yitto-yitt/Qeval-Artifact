# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    with qml.tape.QuantumTape() as tape:
        for pauli_string, time in zip(pauli_strings, times):
            # Qiskit uses little-endian for Pauli strings, PennyLane uses big-endian (left-to-right)
            pl_string = pauli_string[::-1]
            
            active_wires = []
            active_paulis = []
            for i, p in enumerate(pl_string):
                if p != 'I':
                    active_wires.append(i)
                    active_paulis.append(p)
                    
            if not active_paulis:
                for _ in range(reps):
                    qml.GlobalPhase(time / reps)
            else:
                pauli_word = "".join(active_paulis)
                for _ in range(reps):
                    qml.PauliRot(2 * time / reps, pauli_word, wires=active_wires)
                    
    return tape
