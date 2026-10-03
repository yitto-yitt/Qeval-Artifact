# EVAL_META: task_id=110, framework=qiskit, class=3
from operator import index
from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    n = index(n)
    if n < 0:
        raise ValueError("n must be nonnegative.")

    results = []
    for _ in range(n):
        equivalent = circuit.copy()
        if circuit.num_qubits:
            randomizer = random_clifford(circuit.num_qubits).to_circuit()
            equivalent.compose(randomizer, inplace=True)
            equivalent.compose(randomizer.inverse(), inplace=True)
        results.append(equivalent)

    return results
