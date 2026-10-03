# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    ops = []
    for pauli_string, time in zip(pauli_strings, times):
        pauli_ops = []
        for i, p in enumerate(pauli_string):
            if p == 'X':
                pauli_ops.append(qml.PauliX(i))
            elif p == 'Y':
                pauli_ops.append(qml.PauliY(i))
            elif p == 'Z':
                pauli_ops.append(qml.PauliZ(i))
        
        if not pauli_ops:
            op = qml.Identity(0)
        elif len(pauli_ops) == 1:
            op = pauli_ops[0]
        else:
            op = qml.prod(*pauli_ops)
            
        H = qml.Hamiltonian([1.0], [op])
        ops.append(qml.TrotterProduct(H, time, order=1, n=reps))
        
    return qml.tape.QuantumScript(ops)
