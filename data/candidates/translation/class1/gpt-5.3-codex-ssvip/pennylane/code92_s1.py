# EVAL_META: task_id=92, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def calculate_stabilizer_state_info():
    dev = qml.device("default.qubit", wires=2)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = circuit()
    bitstrings = [format(i, "02b") for i in range(4)]
    probabilities_dict = {b: float(p) for b, p in zip(bitstrings, probs) if not np.isclose(p, 0.0)}
    return probabilities_dict
