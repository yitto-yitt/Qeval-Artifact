# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml

def run_bell_state_simulator():
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
        if isinstance(k, tuple):
            k_str = "".join(str(b) for b in k)
        else:
            k_str = str(k)
        probs[k_str] = v / total
        
    return probs
