# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    
    @qml.qnode(dev)
    def circuit():
        a_str = format(a, '03b')
        b_str = format(b, '03b')
        for i in range(3):
            if a_str[2-i] == '0':
                qml.PauliX(i)
            if b_str[2-i] == '0':
                qml.PauliX(i+3)
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])
        for i in range(3):
            qml.PauliX(i+6)
        return qml.probs(wires=[8, 7, 6])
    
    probs = circuit()
    return {format(i, '03b'): float(probs[i]) for i in range(8) if probs[i] > 1e-6}
