# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    
    @qml.qnode(dev)
    def circuit(a, b):
        a_str = format(a, '03b')
        b_str = format(b, '03b')
        for i in range(3):
            if a_str[2 - i] == '1':
                qml.PauliX(wires=i)
            if b_str[2 - i] == '1':
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.probs(wires=[8, 7, 6])
    
    probs = circuit(a, b)
    result = {}
    for idx, p in enumerate(probs):
        if p > 1e-12:
            result[format(idx, '03b')] = p
    return result
