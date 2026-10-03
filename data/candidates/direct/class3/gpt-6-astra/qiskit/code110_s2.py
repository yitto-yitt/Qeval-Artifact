# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    equivalents = []
    for _ in range(n):
        equivalent = circuit.copy()
        if circuit.num_qubits:
            random_circuit = random_clifford(circuit.num_qubits).to_circuit()
            equivalent.compose(random_circuit, inplace=True)
            equivalent.compose(random_circuit.inverse(), inplace=True)
        equivalents.append(equivalent)
    return equivalents
