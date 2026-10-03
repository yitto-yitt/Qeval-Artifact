# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    with qml.tape.QuantumTape() as tape:
        for pauli_string, time in zip(pauli_strings, times):
            obs = []
            for i, char in enumerate(pauli_string):
                if char == 'X':
                    obs.append(qml.PauliX(i))
                elif char == 'Y':
                    obs.append(qml.PauliY(i))
                elif char == 'Z':
                    obs.append(qml.PauliZ(i))
                elif char == 'I':
                    obs.append(qml.Identity(i))
            if obs:
                H = qml.prod(*obs) if len(obs) > 1 else obs[0]
                qml.TrotterProduct(H, time, order=order, n=reps)
    return tape
