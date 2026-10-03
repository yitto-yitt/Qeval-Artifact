# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    dev = qml.device("default.qubit", wires=9, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(3):
            if a_str[2-i] == '0':
                qml.PauliX(wires=i)
            if b_str[2-i] == '0':
                qml.PauliX(wires=i+3)
                
        for i in range(3):
            qml.Toffoli(wires=[i, i+3, i+6])
            
        for i in range(3):
            qml.PauliX(wires=i+6)
            
        return qml.counts(wires=[8, 7, 6])

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
