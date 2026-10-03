# EVAL_META: task_id=1, framework=pennylane, class=1
import pennylane as qml

def run_bell_state_simulator():
    dev = qml.device("default.qubit", wires=2, shots=1000)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(all_outcomes=True)

    counts = circuit()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if value > 0:
            result[key] = value / total
    return result
