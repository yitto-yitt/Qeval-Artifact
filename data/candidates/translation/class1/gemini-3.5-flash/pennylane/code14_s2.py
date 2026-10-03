# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

def bell_each_shot():
    dev = qml.device("default.qubit", wires=2, shots=10)
    
    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts()
    
    counts = circuit()
    total = sum(counts.values())
    
    res = {}
    for key, value in counts.items():
        if isinstance(key, tuple):
            key_str = "".join(str(x) for x in key)
        else:
            key_str = str(key)
        res[key_str] = value / total
    return res
