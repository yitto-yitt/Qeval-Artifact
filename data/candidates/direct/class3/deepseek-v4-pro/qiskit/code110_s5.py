# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit.quantum_info import random_clifford


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    equivalent_circuits = []

    for idx in range(n):
        random_cliff = random_clifford(num_qubits, seed=idx)
        identity_part = random_cliff.to_circuit()
        identity_inverse = random_cliff.adjoint().to_circuit()

        new_circuit = circuit.copy()
        new_circuit.compose(identity_part, inplace=True)
        new_circuit.compose(identity_inverse, inplace=True)
        equivalent_circuits.append(new_circuit)

    return equivalent_circuits
