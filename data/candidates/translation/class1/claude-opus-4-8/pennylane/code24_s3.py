# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(n)
    qc.compose(oracle, inplace=True)

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        qml.from_qiskit(qc)(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n - 1))

    probs = circuit()
    result = {}
    for i, p in enumerate(probs):
        if p > 1e-12:
            bitstring = format(i, f"0{n-1}b")
            result[bitstring] = float(p)
    return result
