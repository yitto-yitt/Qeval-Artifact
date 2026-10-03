# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml
from collections import Counter

def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.sample(wires=[0, 1])

    samples = bell_circuit()
    counts = Counter("".join(str(int(bit)) for bit in sample) for sample in samples)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
