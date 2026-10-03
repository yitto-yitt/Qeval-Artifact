# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n, shots=None)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for w in range(n):
            qml.Hadamard(wires=w)
        qml.from_qiskit(oracle)()
        for w in range(n):
            qml.Hadamard(wires=w)
        return qml.probs(wires=range(n - 1))

    probs = circuit()
    dist = {}
    for i, p in enumerate(probs):
        if p > 0:
            bitstring = format(i, f"0{n-1}b")
            dist[bitstring] = float(p)
    return dist
