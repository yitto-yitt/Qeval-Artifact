# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    dev = qml.device("default.qubit", wires=9)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bin[2-i] == '0':
                qml.PauliX(wires=i)
            if b_bin[2-i] == '0':
                qml.PauliX(wires=3+i)
                
        for i in range(3):
            qml.Toffoli(wires=[i, 3+i, 6+i])
            
        for i in range(3):
            qml.PauliX(wires=6+i)
            
        return qml.probs(wires=[8, 7, 6])

    probs = circuit()
    dist = {}
    for i in range(8):
        if probs[i] > 1e-9:
            dist[format(i, '03b')] = float(probs[i])
    return dist
