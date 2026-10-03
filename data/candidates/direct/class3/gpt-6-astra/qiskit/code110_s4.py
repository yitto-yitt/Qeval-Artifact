# EVAL_META: task_id=110, framework=qiskit, class=3
from operator import index

from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    n = index(n)
    if n < 0:
        raise ValueError("n must be nonnegative.")

    circuits = []
    for _ in range(n):
        equivalent = circuit.copy()
        if circuit.num_qubits:
            dressing = random_clifford(circuit.num_qubits).to_circuit()
            equivalent.compose(dressing, front=True, inplace=True)
            equivalent.compose(dressing.inverse(), front=True, inplace=True)
        circuits.append(equivalent)

    return circuits
