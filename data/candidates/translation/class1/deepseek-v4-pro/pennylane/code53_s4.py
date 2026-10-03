# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)
    target = (a ^ b) & 0xFF

    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if (target >> i) & 1:
                qml.PauliX(wires=i)
        return qml.counts(wires=list(range(7, -1, -1)))

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
