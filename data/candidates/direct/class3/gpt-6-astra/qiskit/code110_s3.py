# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    equivalents = []
    for _ in range(n):
        result = circuit.copy()
        if circuit.num_qubits:
            randomizer = random_clifford(circuit.num_qubits).to_circuit()
            result.compose(randomizer, front=True, inplace=True)
            result.compose(randomizer.inverse(), front=True, inplace=True)
        equivalents.append(result)
    return equivalents
