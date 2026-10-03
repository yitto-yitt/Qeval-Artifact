# EVAL_META: task_id=116, framework=pennylane, class=3
import pennylane as qml

def synthesize_evolution_gate(pauli_string, time):
    ops = []
    for i, char in enumerate(pauli_string):
        if char == 'X':
            ops.append(qml.PauliX(i))
        elif char == 'Y':
            ops.append(qml.PauliY(i))
        elif char == 'Z':
            ops.append(qml.PauliZ(i))
    
    if not ops:
        H = qml.Identity(0)
    else:
        H = ops[0]
        for op in ops[1:]:
            H = H @ op
            
    return qml.exp(H, -1j * time)
