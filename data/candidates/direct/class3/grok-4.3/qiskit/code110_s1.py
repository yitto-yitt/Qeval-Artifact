# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    result = []
    for _ in range(n):
        rand_clifford = random_clifford(num_qubits)
        rand_circuit = rand_clifford.to_circuit()
        inv_circuit = rand_clifford.adjoint().to_circuit()
        new_circuit = circuit.copy()
        new_circuit.compose(rand_circuit, inplace=True)
        new_circuit.compose(inv_circuit, inplace=True)
        result.append(new_circuit)
    return result
