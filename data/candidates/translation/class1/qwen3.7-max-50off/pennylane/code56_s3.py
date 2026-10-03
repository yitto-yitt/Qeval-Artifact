# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    a_bin = format(a, "08b")
    dev = qml.device("default.qubit", wires=8, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a_bin[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.counts(wires=[7, 6, 5, 4, 3, 2, 1, 0])
    
    counts = circuit()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
