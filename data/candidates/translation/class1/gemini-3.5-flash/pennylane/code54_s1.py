# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)

    @qml.qnode(dev)
    def circuit(a_str, b_str):
        for i in range(3):
            if a_str[2 - i] == '1':
                qml.PauliX(i)
            if b_str[2 - i] == '1':
                qml.PauliX(3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.probs(wires=[8, 7, 6])

    a_str = format(a, '03b')
    b_str = format(b, '03b')
    probs = circuit(a_str, b_str)
    
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-6:
            result[format(i, '03b')] = float(p)
    return result
