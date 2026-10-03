# EVAL_META: task_id=92, framework=pennylane, class=1
import pennylane as qml

def calculate_stabilizer_state_info():
    device = qml.device("default.qubit", wires=2)

    @qml.qnode(device)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[1, 0])

    probabilities = circuit()
    return {
        format(index, "02b"): float(probability)
        for index, probability in enumerate(probabilities)
        if probability > 0
    }
