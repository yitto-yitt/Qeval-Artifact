# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        a_str = format(a, "08b")
        for j in range(8):
            if a_str[j] == "0":
                qml.PauliX(wires=j)
        return qml.probs(wires=range(8))
    
    probs = circuit()
    
    result = {}
    for idx, prob in enumerate(probs):
        if prob > 1e-6:
            bitstring = format(idx, "08b")
            result[bitstring] = float(prob)
    return result
