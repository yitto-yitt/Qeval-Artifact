# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device('default.qubit', wires=9)
    
    @qml.qnode(dev)
    def circuit(a_val, b_val):
        a_str = format(a_val, '03b')
        b_str = format(b_val, '03b')
        
        for i in range(3):
            if a_str[2-i] == '1':
                qml.PauliX(wires=i)
            if b_str[2-i] == '1':
                qml.PauliX(wires=i + 3)
                
        for i in range(3):
            qml.Toffoli(wires=[i, i + 3, i + 6])
            
        return qml.probs(wires=[8, 7, 6])
    
    probs = circuit(a, b)
    
    result = {}
    for i, prob in enumerate(probs):
        if prob > 1e-6:
            bitstring = format(i, '03b')
            result[bitstring] = float(prob)
            
    return result
