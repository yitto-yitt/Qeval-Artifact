# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device('default.qubit', wires=8, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        a_bin = format(a, "08b")
        for i in range(8):
            if a_bin[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))
    
    samples = circuit()
    counts = {}
    for sample in samples:
        key = ''.join(str(int(b)) for b in sample)
        counts[key] = counts.get(key, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
