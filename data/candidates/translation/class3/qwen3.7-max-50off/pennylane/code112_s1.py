# EVAL_META: task_id=112, framework=pennylane, class=3
import pennylane as qml

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_wires = len(pauli_strings[0])
    wires = list(range(num_wires))
    
    with qml.queuing.AnnotatedQueue() as q:
        for pauli_string, time in zip(pauli_strings, times):
            ops = []
            for char, w in zip(pauli_string, wires):
                if char == 'X':
                    ops.append(qml.PauliX(w))
                elif char == 'Y':
                    ops.append(qml.PauliY(w))
                elif char == 'Z':
                    ops.append(qml.PauliZ(w))
            
            if not ops:
                obs = qml.Identity(wires[0])
            else:
                obs = ops[0] if len(ops) == 1 else qml.prod(*ops)
            
            H = qml.Hamiltonian([1.0], [obs])
            qml.TrotterProduct(H, time, order=1, n=reps)
            
    return qml.tape.QuantumScript.from_queue(q)
