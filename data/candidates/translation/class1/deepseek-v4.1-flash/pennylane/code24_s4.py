# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
        qml.from_qiskit(oracle)()
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n-2, -1, -1))
    probs = circuit()
    num_inputs = n - 1
    dist = {}
    for i, p in enumerate(probs):
        bitstring = format(i, f'0{num_inputs}b')
        dist[bitstring] = float(p)
    return dist
