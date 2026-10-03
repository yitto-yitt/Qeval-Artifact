# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    dev = qml.device("default.mixed", wires=2, shots=1000)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        qml.DepolarizingChannel(0.01, wires=0)
        qml.DepolarizingChannel(0.01, wires=1)
        return qml.counts()

    counts = bell_circuit()
    total = sum(counts.values())
    return {bitstring: count / total for bitstring, count in counts.items()}
