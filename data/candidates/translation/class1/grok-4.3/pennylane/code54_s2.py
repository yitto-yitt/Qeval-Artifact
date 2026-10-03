# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, '03b')
        for i in range(3):
            if a_bin[2 - i] == '1':
                qml.PauliX(wires=i)
        b_bin = format(b, '03b')
        for i in range(3):
            if b_bin[2 - i] == '1':
                qml.PauliX(wires=3 + i)
        for i in range(3):
            qml.Toffoli(wires=[i, 3 + i, 6 + i])
        return qml.probs(wires=[8, 7, 6])
    probs = circuit()
    n = 3
    result = {}
    for i in range(2 ** n):
        if probs[i] > 1e-10:
            key = format(i, f'0{n}b')
            result[key] = float(probs[i])
    return result
