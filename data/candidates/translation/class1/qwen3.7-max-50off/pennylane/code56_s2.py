# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    a_bin = format(a, "08b")
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a_bin[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=[7, 6, 5, 4, 3, 2, 1, 0])
    
    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            result[format(i, "08b")] = float(p)
    return result
