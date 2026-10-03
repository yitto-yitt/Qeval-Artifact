# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        val = a ^ b
        for i in range(8):
            if (val >> i) & 1:
                qml.PauliX(wires=i)
        return qml.counts(wires=[7, 6, 5, 4, 3, 2, 1, 0])
    
    counts = circuit()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if isinstance(key, str):
            k_str = key
        elif isinstance(key, int):
            k_str = f"{key:08b}"
        else:
            k_str = "".join(str(bit) for bit in key)
        result[k_str] = value / total
    return result
