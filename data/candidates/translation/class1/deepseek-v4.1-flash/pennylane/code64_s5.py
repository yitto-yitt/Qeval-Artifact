# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    dev = qml.device("default.qubit", wires=2 * n if n > 0 else 1)

    @qml.qnode(dev)
    def circuit():
        for k in range(n):
            qml.Hadamard(wires=k)
        for k in range(n):
            qml.CNOT(wires=[k, n + k])
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n + j])
            for k in range(n):
                qml.Hadamard(wires=k)
        return qml.probs(wires=list(range(n)))

    return circuit
