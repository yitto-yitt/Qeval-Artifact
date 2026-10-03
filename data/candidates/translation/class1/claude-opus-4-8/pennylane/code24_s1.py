# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits
    dev = qml.device("default.qubit", wires=n)

    ops = qml.from_qiskit(oracle)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        ops(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n - 1))

    probs = circuit()
    result = {}
    for idx, p in enumerate(probs):
        if p > 1e-12:
            bitstring = format(idx, "0{}b".format(n - 1))
            result[bitstring] = float(p)
    return result
