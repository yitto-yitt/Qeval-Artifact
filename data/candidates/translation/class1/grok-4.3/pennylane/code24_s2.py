# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for wire in range(n):
            qml.Hadamard(wires=wire)
        oracle(wires=range(n))
        for wire in range(n):
            qml.Hadamard(wires=wire)
        return qml.probs(wires=range(n-1))
    probs = circuit()
    bit_length = n - 1
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-10:
            key = format(i, f'0{bit_length}b')
            result[key] = float(p)
    return result
