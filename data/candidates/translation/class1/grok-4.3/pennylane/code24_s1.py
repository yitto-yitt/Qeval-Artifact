# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    with qml.tape.QuantumTape() as tape:
        oracle()
    wires = tape.wires
    n = max(wires) + 1 if wires else 1
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
        oracle()
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n-1))
    probs = circuit()
    num_bits = n - 1
    bitstrings = [format(i, f"0{num_bits}b") for i in range(2 ** num_bits)]
    return {bs: float(p) for bs, p in zip(bitstrings, probs) if p > 1e-10}
