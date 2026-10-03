# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    reg1 = list(range(n))
    reg2 = list(range(n, 2 * n))
    all_wires = reg1 + reg2

    ops = []

    for wire in reg1:
        ops.append(qml.Hadamard(wires=wire))

    if all_wires:
        ops.append(qml.Barrier(wires=all_wires))

    for j in range(n):
        ops.append(qml.CNOT(wires=[reg1[j], reg2[j]]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                ops.append(qml.CNOT(wires=[reg1[i], reg2[j]]))

        if all_wires:
            ops.append(qml.Barrier(wires=all_wires))

        for wire in reg1:
            ops.append(qml.Hadamard(wires=wire))

    measurements = [qml.sample(wires=reg1)]
    return qml.tape.QuantumScript(ops, measurements)
