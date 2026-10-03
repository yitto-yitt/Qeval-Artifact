# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, shots=4096, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])
        
    counts = circuit()
    total = sum(counts.values())
    result = {}
    for k, v in counts.items():
        if isinstance(k, str):
            key = k
        else:
            key = "".join(str(b) for b in k)
        result[key] = float(v) / total
    return result
