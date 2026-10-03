# EVAL_META: task_id=15, framework=pennylane, class=1
import pennylane as qml

def noisy_bell():
    dev = qml.device('default.qubit', wires=2)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.probs(wires=[0, 1])
    
    probs = circuit()
    return {format(i, '02b'): p for i, p in enumerate(probs)}
