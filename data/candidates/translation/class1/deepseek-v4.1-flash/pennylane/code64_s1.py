# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml

def simons_algorithm(s):
    n = len(s)
    s_rev = s[::-1]
    ops = []
    for i in range(n):
        ops.append(qml.Hadamard(wires=i))
    ops.append(qml.Barrier(wires=range(n)))
    for i in range(n):
        ops.append(qml.CNOT(wires=[i, n + i]))
    if "1" in s_rev:
        i = s_rev.find("1")
        for j in range(n):
            if s_rev[j] == "1":
                ops.append(qml.CNOT(wires=[i, n + j]))
        ops.append(qml.Barrier(wires=range(n)))
        for i in range(n):
            ops.append(qml.Hadamard(wires=i))
    measurements = [qml.sample(wires=range(n))]
    return qml.tape.QuantumScript(ops, measurements)
