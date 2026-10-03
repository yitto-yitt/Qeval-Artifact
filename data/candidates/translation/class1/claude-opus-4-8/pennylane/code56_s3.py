# EVAL_META: task_id=56, framework=pennylane, class=1
import pennylane as qml

def not_gate(a):
    dev = qml.device('default.qubit', wires=8, shots=1024)
    
    a_binary = format(a, "08b")
    
    @qml.qnode(dev)
    def circuit():
        for i in range(8):
            if a_binary[7-i] == "0":
                qml.PauliX(wires=i)
        return qml.sample(wires=range(8))
    
    samples = circuit()
    
    counts = {}
    for sample in samples:
        bitstring = ''.join(str(int(bit)) for bit in sample)
        counts[bitstring] = counts.get(bitstring, 0) + 1
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
