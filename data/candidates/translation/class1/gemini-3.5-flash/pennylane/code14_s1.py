# EVAL_META: task_id=14, framework=pennylane, class=1
import pennylane as qml

def bell_each_shot():
    dev = qml.device("default.qubit", shots=10)

    @qml.qnode(dev)
    def circuit():
        qml.Hadamard(wires=0)
        qml.CNOT(wires=[0, 1])
        return qml.counts(wires=[0, 1])

    counts = circuit()
    total = sum(counts.values())
    
    def format_key(key):
        if isinstance(key, (list, tuple)):
            return "".join(map(str, key))
        return str(key)
        
    return {format_key(key): value / total for key, value in counts.items()}
