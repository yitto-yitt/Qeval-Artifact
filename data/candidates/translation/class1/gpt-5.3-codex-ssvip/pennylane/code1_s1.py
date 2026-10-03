# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml


def run_bell_state_simulator():
    shots = 1000
    dev = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = bell_circuit()
    counts = {}
    for s in samples:
        bitstring = "".join(str(int(b)) for b in s)
        counts[bitstring] = counts.get(bitstring, 0) + 1

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
