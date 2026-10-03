# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    a_str = format(a, "08b")
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a_str[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=list(range(8)))
    
    probs = circuit()
    result = {}
    for i in range(256):
        if probs[i] > 1e-9:
            result[format(i, "08b")] = float(probs[i])
    return result
