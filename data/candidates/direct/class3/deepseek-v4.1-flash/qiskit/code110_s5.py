# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford

def equivalent_clifford_circuit(circuit, n):
    num_qubits = circuit.num_qubits
    if num_qubits == 0:
        return [circuit.copy() for _ in range(n)]
    result = []
    for _ in range(n):
        rand_cliff = random_clifford(num_qubits)
        rand_circ = rand_cliff.to_circuit()
        inv_circ = rand_cliff.adjoint().to_circuit()
        new_circ = circuit.compose(rand_circ).compose(inv_circ)
        result.append(new_circ)
    return result
