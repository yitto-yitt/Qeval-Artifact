# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, shots=4096, seed=42)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()

    counts = bell_circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
