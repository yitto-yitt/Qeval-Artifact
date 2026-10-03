# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    results = []

    for _ in range(n):
        rand_cliff = random_clifford(num_qubits)
        rand_circuit = rand_cliff.to_circuit()
        inv_circuit = rand_cliff.adjoint().to_circuit()

        new_circuit = QuantumCircuit(num_qubits)
        new_circuit.compose(inv_circuit, inplace=True)
        new_circuit.compose(rand_circuit, inplace=True)
        new_circuit.compose(circuit, inplace=True)

        results.append(new_circuit)

    return results
