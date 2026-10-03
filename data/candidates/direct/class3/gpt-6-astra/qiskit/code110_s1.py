# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    equivalents = []
    for _ in range(n):
        equivalent = circuit.copy()
        if circuit.num_qubits:
            random_layer = random_clifford(circuit.num_qubits).to_circuit()
            qubits = list(range(circuit.num_qubits))
            equivalent.compose(
                random_layer, qubits=qubits, front=True, inplace=True
            )
            equivalent.compose(
                random_layer.inverse(), qubits=qubits, front=True, inplace=True
            )
        equivalents.append(equivalent)
    return equivalents
