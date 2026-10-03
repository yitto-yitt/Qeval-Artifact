# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit(a):
        a_str = format(a, "08b")
        for i in range(8):
            if a_str[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    
    probs = circuit(a)
    
    result = {}
    for idx, prob in enumerate(probs):
        if prob > 1e-5:
            bin_str = format(idx, "08b")
            qiskit_str = bin_str[::-1]
            result[qiskit_str] = float(prob)
            
    return result
