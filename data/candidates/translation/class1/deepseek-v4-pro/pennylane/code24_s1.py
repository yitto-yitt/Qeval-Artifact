# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = getattr(oracle, "num_wires", None)
    if n is None:
        n = len(oracle.wires)
    m = n - 1

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for w in range(n):
            qml.Hadamard(wires=w)

        if callable(oracle):
            oracle(wires=list(range(n)))
        else:
            for op in oracle.operations:
                qml.apply(op)

        for w in range(n):
            qml.Hadamard(wires=w)

        return qml.probs(wires=list(range(m)))

    probs = circuit()
    dist = {}
    for i, p in enumerate(probs):
        if p > 0:
            dist[format(i, f"0{m}b")[::-1]] = float(p)
    return dist
