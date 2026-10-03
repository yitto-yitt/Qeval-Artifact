# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    bits = format(a, "08b")
    device = qml.device("default.qubit", wires=8)

    @qml.set_shots(shots=1024)
    @qml.qnode(device)
    def circuit():
        for i in range(8):
            if bits[7 - i] == "0":
                qml.PauliX(wires=i)
        return qml.counts(wires=list(range(7, -1, -1)))

    counts = circuit()
    total = sum(counts.values())
    return {key: int(value) / total for key, value in counts.items()}
