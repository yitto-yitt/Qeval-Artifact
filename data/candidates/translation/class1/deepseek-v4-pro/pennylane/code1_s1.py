# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml

def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = bell_circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
