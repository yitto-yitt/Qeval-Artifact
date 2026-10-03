# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n, shots=1024)

    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            if (a >> i) & 1:
                qml.PauliX(wires=n - 1 - i)
        for i in range(n):
            if (b >> i) & 1:
                qml.PauliX(wires=n - 1 - i)
        return qml.counts(all_outcomes=True)

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items() if value > 0}
