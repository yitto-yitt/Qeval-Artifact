# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_wires
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
        oracle(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n-1))
    probs = circuit()
    m = n - 1
    bitstrings = [format(i, f"0{m}b") for i in range(1 << m)]
    return {bs: float(p) for bs, p in zip(bitstrings, probs)}
