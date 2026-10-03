# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    reg1 = list(range(n))
    reg2 = list(range(n, 2 * n))

    dev = qml.device("default.qubit", wires=2 * n)

    @qml.qnode(dev)
    def circuit():
        for wire in reg1:
            qml.Hadamard(wires=wire)

        for j in range(n):
            qml.CNOT(wires=[reg1[j], reg2[j]])

        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[reg1[i], reg2[j]])

            for wire in reg1:
                qml.Hadamard(wires=wire)

        return qml.probs(wires=reg1)

    return circuit
