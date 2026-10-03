# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    
    @qml.qnode(dev)
    def circuit(a_int, b_int):
        a_str = format(a_int, '03b')
        b_str = format(b_int, '03b')
        
        for i in range(3):
            if a_str[2-i] == '0':
                qml.PauliX(wires=i)
            if b_str[2-i] == '0':
                qml.PauliX(wires=3+i)
                
        for i in range(3):
            qml.Toffoli(wires=[i, 3+i, 6+i])
            
        for i in range(3):
            qml.PauliX(wires=6+i)
            
        return qml.probs(wires=[8, 7, 6])

    probs = circuit(a, b)
    
    result = {}
    for i in range(8):
        bitstring = format(i, '03b')
        result[bitstring] = float(probs[i])
        
    return result
