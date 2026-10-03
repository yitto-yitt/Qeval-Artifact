# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = len(oracle.wires)
    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        for op in oracle.operations:
            qml.apply(op)
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n - 2, -1, -1))

    probs = circuit()
    return {format(i, f'0{n - 1}b'): probs[i] for i in range(2 ** (n - 1))}
