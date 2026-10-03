# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford


def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    num_clbits = circuit.num_clbits
    results = []
    for _ in range(n):
        R = random_clifford(num_qubits)
        R_inv = R.adjoint()

        r_inv_circ = R_inv.to_circuit()
        r_circ = R.to_circuit()

        new_circuit = QuantumCircuit(num_qubits, num_clbits)
        new_circuit = new_circuit.compose(r_inv_circ, qubits=range(num_qubits))
        new_circuit = new_circuit.compose(r_circ, qubits=range(num_qubits))
        new_circuit = new_circuit.compose(
            circuit, qubits=range(num_qubits), clbits=range(num_clbits)
        )

        results.append(new_circuit)

    return results
