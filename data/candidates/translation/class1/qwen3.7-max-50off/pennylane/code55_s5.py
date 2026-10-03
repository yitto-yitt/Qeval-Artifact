# EVAL_META: task_id=55, framework=pennylane, class=1
import pennylane as qml

def or_gate(a, b):
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    dev = qml.device("default.qubit", wires=9, shots=1000)
    
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
            
        return qml.counts(wires=[8, 7, 6])
        
    counts = circuit()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if isinstance(key, int):
            k = format(key, '03b')
        elif isinstance(key, tuple):
            k = "".join(str(bit) for bit in key)
        else:
            k = str(key)
        result[k] = value / total
    return result
