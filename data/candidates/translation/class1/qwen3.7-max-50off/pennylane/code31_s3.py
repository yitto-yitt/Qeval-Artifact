# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, shots=4096, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])
        
    samples = circuit()
    counts = {}
    for s in samples:
        key = f"{int(s[0])}{int(s[1])}"
        counts[key] = counts.get(key, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
