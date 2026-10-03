# EVAL_META: task_id=54, framework=pennylane, class=1
import pennylane as qml

def and_gate(a, b):
    dev = qml.device("default.qubit", wires=9)
    
    @qml.qnode(dev)
    def circuit():
        a_bits = format(a, '03b')
        b_bits = format(b, '03b')
        
        if a_bits[2] == '1': qml.PauliX(wires=0)
        if a_bits[1] == '1': qml.PauliX(wires=1)
        if a_bits[0] == '1': qml.PauliX(wires=2)
            
        if b_bits[2] == '1': qml.PauliX(wires=3)
        if b_bits[1] == '1': qml.PauliX(wires=4)
        if b_bits[0] == '1': qml.PauliX(wires=5)
            
        qml.Toffoli(wires=[0, 3, 6])
        qml.Toffoli(wires=[1, 4, 7])
        qml.Toffoli(wires=[2, 5, 8])
        
        return qml.probs(wires=[8, 7, 6])
        
    probs = circuit()
    return {format(i, '03b'): float(probs[i]) for i in range(8) if probs[i] > 1e-9}
