# EVAL_META: task_id=53, framework=pennylane, class=1
import pennylane as qml

def xor_gate(a, b):
    n = 8
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        for pos in range(n):
            bit_a = (a >> pos) & 1
            bit_b = (b >> pos) & 1
            wire = n - 1 - pos
            if bit_a:
                qml.X(wires=wire)
            if bit_b:
                qml.X(wires=wire)
        return qml.probs(wires=range(n))

    probs = circuit()
    result = {}
    for k, p in enumerate(probs):
        if p > 1e-10:
            bin_str = format(k, f"0{n}b")
            result[bin_str] = float(p)
    return result
