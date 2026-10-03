# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2, seed=42)

    @qml.qnode(dev)
    def bell_circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])

    probs = bell_circuit()
    bitstrings = ["00", "01", "10", "11"]
    return {bs: float(prob) for bs, prob in zip(bitstrings, probs) if prob > 0}
