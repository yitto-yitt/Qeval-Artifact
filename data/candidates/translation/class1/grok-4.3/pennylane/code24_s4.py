# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits
    oracle_pl = qml.from_qiskit(oracle)
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for w in range(n):
            qml.Hadamard(wires=w)
        oracle_pl(wires=list(range(n)))
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.probs(wires=range(n-1))
    probs = circuit()
    m = n - 1
    bitstrings = [bin(i)[2:].zfill(m) for i in range(2 ** m)]
    dist = {}
    for bs, p in zip(bitstrings, probs):
        dist[bs[::-1]] = float(p)
    return dist
