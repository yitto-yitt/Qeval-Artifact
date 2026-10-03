# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford
import random

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    result = []
    for _ in range(n):
        new_circuit = circuit.copy()
        num_pairs = random.randint(1, 3)
        for __ in range(num_pairs):
            rc = random_clifford(num_qubits)
            rand_circuit = rc.to_circuit()
            inv_circuit = rc.adjoint().to_circuit()
            new_circuit = new_circuit.compose(rand_circuit)
            new_circuit = new_circuit.compose(inv_circuit)
        result.append(new_circuit)
    return result
