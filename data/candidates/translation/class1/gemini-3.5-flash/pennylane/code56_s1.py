# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit(a):
        a_str = format(a, "08b")
        for i in range(8):
            if a_str[i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    
    probs = circuit(a)
    return {format(i, "08b"): float(probs[i]) for i in range(256) if probs[i] > 1e-6}
