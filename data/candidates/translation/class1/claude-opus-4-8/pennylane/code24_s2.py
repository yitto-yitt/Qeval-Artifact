# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml

def dj_algorithm(oracle):
    n = oracle.num_qubits

    from qiskit import QuantumCircuit
    if not isinstance(oracle, QuantumCircuit):
        raise TypeError("oracle must be a QuantumCircuit")

    dev = qml.device("default.qubit", wires=n)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        qml.from_qiskit(oracle)(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.probs(wires=range(n - 1))

    probs = circuit()

    result = {}
    m = n - 1
    for idx, p in enumerate(probs):
        if p > 1e-12:
            key = format(idx, f"0{m}b")
            result[key] = float(p)

    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
