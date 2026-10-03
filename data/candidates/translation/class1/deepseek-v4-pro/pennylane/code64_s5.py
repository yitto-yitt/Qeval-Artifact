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
        for q in reg1:
            qml.Hadamard(wires=q)
        qml.Barrier(wires=reg1 + reg2)

        for q1, q2 in zip(reg1, reg2):
            qml.CNOT(wires=[q1, q2])

        if "1" in s:
            ctrl = s.find("1")
            for j, bit in enumerate(s):
                if bit == "1":
                    qml.CNOT(wires=[reg1[ctrl], reg2[j]])

            qml.Barrier(wires=reg1 + reg2)
            for q in reg1:
                qml.Hadamard(wires=q)

        return qml.probs(wires=reg1)

    return circuit
