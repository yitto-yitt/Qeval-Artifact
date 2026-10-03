# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    dev = qml.device("default.qubit", wires=2, shots=1000)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[1, 0])
    
    probs = circuit()
    bitstrings = ['00', '01', '10', '11']
    result = {bitstrings[i]: float(probs[i]) for i in range(4) if probs[i] > 0}
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
