# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml

def simons_algorithm(s):
    n = len(s)
    s_rev = s[::-1]
    dev = qml.device("default.qubit", wires=2 * n)

    @qml.qnode(dev)
    def circuit():
        for k in range(n):
            qml.Hadamard(wires=k)
        qml.Barrier(wires=range(2 * n))
        for k in range(n):
            qml.CNOT(wires=[k, n + k])
        if "1" in s_rev:
            i = s_rev.find("1")
            for j in range(n):
                if s_rev[j] == "1":
                    qml.CNOT(wires=[i, n + j])
            qml.Barrier(wires=range(2 * n))
            for k in range(n):
                qml.Hadamard(wires=k)
        return qml.sample(wires=range(n))

    return circuit
