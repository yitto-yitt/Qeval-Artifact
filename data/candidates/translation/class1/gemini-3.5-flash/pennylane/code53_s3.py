# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device('default.qubit', wires=8)
    
    @qml.qnode(dev)
    def circuit():
        # Apply XOR for a
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(i)
        # Apply XOR for b
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(i)
        return qml.probs(wires=list(range(7, -1, -1)))
    
    probs = circuit()
    return {f"{i:08b}": float(probs[i]) for i in range(256) if probs[i] > 0}
