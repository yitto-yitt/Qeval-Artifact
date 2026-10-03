# EVAL_META: task_id=31, framework=pennylane, class=1
import pennylane as qml

def sampler_qiskit():
    dev = qml.device("default.qubit", wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
        
    probs = circuit()
    bitstrings = ['00', '01', '10', '11']
    return {bs: float(p) for bs, p in zip(bitstrings, probs) if p > 1e-9}
