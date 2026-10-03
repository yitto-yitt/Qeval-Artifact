# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    reg1 = [f"reg1_{i}" for i in range(n)]
    reg2 = [f"reg2_{i}" for i in range(n)]
    wires = reg1 + reg2

    dev = qml.device("default.qubit", wires=wires)

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
