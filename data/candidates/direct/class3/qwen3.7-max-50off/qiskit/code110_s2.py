# EVAL_META: task_id=110, framework=qiskit, class=3

from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    cliff = Clifford(circuit)
    base = cliff.to_circuit()
    results = []

    for _ in range(n):
        R = random_clifford(num_qubits)
        R_inv = R.adjoint()

        new_circ = QuantumCircuit(num_qubits)
        new_circ.compose(R_inv.to_circuit(), inplace=True)
        new_circ.compose(R.to_circuit(), inplace=True)
        new_circ.compose(base, inplace=True)

        results.append(new_circ)

    return results
