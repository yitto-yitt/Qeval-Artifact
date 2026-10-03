# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford


def _clifford_to_circuit(cliff):
    try:
        return cliff.to_circuit()
    except Exception:
        from qiskit.synthesis import synthesize_clifford
        return synthesize_clifford(cliff)


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    if num_qubits == 0:
        return [circuit.copy() for _ in range(n)]

    target_cliff = Clifford(circuit)
    results = []

    for i in range(n):
        rand_cliff = random_clifford(num_qubits, seed=i * 7 + 13)
        rand_circ = _clifford_to_circuit(rand_cliff)

        inv_rand = rand_cliff.adjoint()
        modified = inv_rand.compose(target_cliff)
        modified_circ = _clifford_to_circuit(modified)

        combined = QuantumCircuit(num_qubits)
        combined.compose(modified_circ, inplace=True)
        combined.compose(rand_circ, inplace=True)

        results.append(combined)

    return results
