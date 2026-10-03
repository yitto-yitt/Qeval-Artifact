# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit(a, b):
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=7 - i)
        for i in range(8):
            if (b >> i) & 1:
                qml.PauliX(wires=7 - i)
        return qml.probs(wires=range(8))
    
    probs = circuit(a, b)
    
    result = {}
    for idx, prob in enumerate(probs):
        if prob > 1e-6:
            bin_str = f"{idx:08b}"
            result[bin_str] = float(prob)
    return result
