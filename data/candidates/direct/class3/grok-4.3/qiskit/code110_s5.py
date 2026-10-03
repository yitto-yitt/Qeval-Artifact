# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    equivalents = []
    for _ in range(n):
        new_circuit = circuit.copy()
        rand_clifford = random_clifford(num_qubits)
        rand_circuit = rand_clifford.to_circuit()
        inv_circuit = rand_clifford.adjoint().to_circuit()
        new_circuit.compose(rand_circuit, inplace=True)
        new_circuit.compose(inv_circuit, inplace=True)
        equivalents.append(new_circuit)
    return equivalents
