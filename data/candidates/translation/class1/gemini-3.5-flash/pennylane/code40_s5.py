# EVAL_META: task_id=40, framework=pennylane, class=1
import pennylane as qml

def init_random_3qubit(desired_vector):
    dev = qml.device("default.qubit", wires=3, shots=1024, seed=42)
    
    @qml.qnode(dev)
    def circuit():
        qml.StatePrep(desired_vector, wires=[0, 1, 2])
        return qml.counts(wires=[0, 1, 2])
    
    counts = circuit()
    total = sum(counts.values())
    
    res = {}
    for key, value in counts.items():
        if isinstance(key, tuple):
            str_key = "".join(map(str, key))
        else:
            str_key = str(key)
        res[str_key] = value / total
    return res
