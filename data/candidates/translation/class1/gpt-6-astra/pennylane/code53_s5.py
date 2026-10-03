# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    device = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        for value in (a, b):
            for wire in range(8):
                if (value >> wire) & 1:
                    qml.PauliX(wires=wire)
        return qml.counts(wires=list(reversed(range(8))))

    counts = circuit()
    total = sum(counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
