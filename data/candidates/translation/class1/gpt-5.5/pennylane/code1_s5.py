# EVAL_META: task_id=1, framework=pennylane, class=1
from collections import Counter
import pennylane as qml

def run_bell_state_simulator():
    shots = 1000
    dev = qml.device("default.qubit", wires=2, shots=shots)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = circuit()
    counts = Counter("".join(str(int(bit)) for bit in sample) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
