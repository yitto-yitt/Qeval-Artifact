# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    c = a ^ b
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (c >> i) & 1:
                qml.PauliX(wires=7 - i)
        return qml.probs(wires=range(8))
    
    probs = circuit()
    
    result = {}
    for idx, p in enumerate(probs):
        if p > 0:
            key = f"{idx:08b}"
            result[key] = float(p)
            
    return result
