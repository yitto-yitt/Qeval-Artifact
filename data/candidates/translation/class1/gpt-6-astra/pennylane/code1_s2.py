# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml

def run_bell_state_simulator():
    device = qml.device("default.qubit", wires=2)

    @qml.set_shots(shots=1000)
    @qml.qnode(device)
    @qml.transforms.compile
    def bell():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[1, 0])

    counts = bell()
    total = sum(counts.values())
    return {str(key): int(value) / total for key, value in counts.items()}
