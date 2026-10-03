# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    dev = qml.device("default.qubit", wires=8)
    
    @qml.qnode(dev)
    def circuit():
        val = a ^ b
        for i in range(8):
            bit = (val >> (7 - i)) & 1
            if bit:
                qml.PauliX(wires=i)
        return qml.probs(wires=range(8))
    
    probs = circuit()
    res = {}
    for idx, p in enumerate(probs):
        if p > 1e-6:
            bitstring = f"{idx:08b}"
            res[bitstring] = float(p)
    return res
