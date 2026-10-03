# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
from pennylane import numpy as np

def dj_algorithm(oracle):
    n = oracle.num_qubits

    from qiskit import QuantumCircuit
    oc = QuantumCircuit(n)
    oc.compose(oracle, inplace=True)

    dev = qml.device("default.qubit", wires=n, shots=10000)

    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n - 1)
        for i in range(n):
            qml.Hadamard(wires=i)
        qml.from_qiskit(oc)(wires=range(n))
        for i in range(n):
            qml.Hadamard(wires=i)
        return qml.counts(wires=range(n - 1))

    counts = circuit()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
