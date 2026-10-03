# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (a >> i) & 1:
                qml.PauliX(wires=7 - i)
            if (b >> i) & 1:
                qml.PauliX(wires=7 - i)
        return qml.counts(wires=range(8))
    
    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
