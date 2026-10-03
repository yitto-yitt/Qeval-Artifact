# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    dev = qml.device("default.qubit", wires=2 * n, shots=1)

    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            qml.Hadamard(wires=i)
        for i in range(n):
            qml.CNOT(wires=[i, n + i])
        if "1" in s:
            idx = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[idx, n + j])
            for i in range(n):
                qml.Hadamard(wires=i)
        return qml.sample(wires=range(n))

    return circuit
