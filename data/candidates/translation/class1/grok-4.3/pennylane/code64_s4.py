# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    dev = qml.device("default.qubit", wires=2*n, shots=1024)
    @qml.qnode(dev)
    def qcircuit():
        for i in range(n):
            qml.Hadamard(i)
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        if "1" in s:
            i_pos = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i_pos, n+j])
            for k in range(n):
                qml.Hadamard(k)
        return qml.sample(wires=range(n))
    return qcircuit
