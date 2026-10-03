# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        val = a ^ b
        for i in range(8):
            if (val >> i) & 1:
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))
    
    samples = circuit()
    counts = {}
    for s in samples:
        qiskit_key = "".join(str(int(bit)) for bit in s[::-1])
        counts[qiskit_key] = counts.get(qiskit_key, 0) + 1
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
