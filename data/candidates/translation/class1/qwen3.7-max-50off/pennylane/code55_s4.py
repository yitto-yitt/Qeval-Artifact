# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_bin[2-i] == '0':
                qml.PauliX(wires=i)
            if b_bin[2-i] == '0':
                qml.PauliX(wires=i+3)
                
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])
            
        for i in range(3):
            qml.PauliX(wires=i+6)
            
        return qml.probs(wires=[6, 7, 8])

    probs = circuit()
    
    result_dict = {}
    for i in range(8):
        if probs[i] > 1e-5:
            w6 = (i >> 2) & 1
            w7 = (i >> 1) & 1
            w8 = i & 1
            key = f"{w8}{w7}{w6}"
            result_dict[key] = float(probs[i])
            
    return result_dict
