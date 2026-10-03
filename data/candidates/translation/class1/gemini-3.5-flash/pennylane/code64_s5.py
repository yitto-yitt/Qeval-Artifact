# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=2 * n, shots=1)

    @qml.qnode(dev)
    def circuit():
        s_rev = s[::-1]

        for k in range(n):
            qml.Hadamard(wires=k)

        for k in range(n):
            qml.CNOT(wires=[k, n + k])

        if "1" in s_rev:
            i = s_rev.find("1")
            for j in range(n):
                if s_rev[j] == "1":
                    qml.CNOT(wires=[i, n + j])

        for k in range(n):
            qml.Hadamard(wires=k)

        return qml.sample(wires=range(n))

    return circuit
