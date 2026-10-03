# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = bell_circuit()
    counts = {}
    for sample in samples:
        bitstring = "".join(str(int(s)) for s in sample)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = len(samples)
    return {k: v / total for k, v in counts.items()}
