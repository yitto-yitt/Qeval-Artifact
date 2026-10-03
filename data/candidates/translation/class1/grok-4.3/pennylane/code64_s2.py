# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml
def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    dev = qml.device("default.qubit", wires=2*n, shots=1)
    @qml.qnode(dev)
    def circuit():
        for wire in range(n):
            qml.Hadamard(wires=wire)
        for wire in range(n):
            qml.CNOT(wires=[wire, n + wire])
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, n + j])
            for wire in range(n):
                qml.Hadamard(wires=wire)
        return qml.sample(wires=range(n))
    return circuit()
