# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    dev = qml.device("default.qubit", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])
    
    counts = circuit()
    total = sum(counts.values())
    
    probs = {}
    for k, v in counts.items():
        key_str = "".join(map(str, k)) if isinstance(k, tuple) else str(k)
        probs[key_str] = v / total
        
    return probs
