# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

dev = qml.device("default.qubit", wires=2, shots=10)

@qml.qnode(dev)
def circuit():
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0, 1])
    return qml.counts(wires=[0, 1])

def bell_each_shot():
    counts = circuit()
    total = sum(counts.values())
    # Reverse keys to match Qiskit's little-endian bitstring convention
    return {k[::-1]: v / total for k, v in counts.items()}
