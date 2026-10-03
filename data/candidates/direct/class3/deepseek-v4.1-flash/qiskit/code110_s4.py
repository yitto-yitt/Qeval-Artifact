# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford, Clifford

def equivalent_clifford_circuit(circuit, n):
    if isinstance(circuit, Clifford):
        base_circuit = circuit.to_circuit()
    else:
        base_circuit = circuit
    num_qubits = base_circuit.num_qubits
    result = []
    for _ in range(n):
        rand_cliff = random_clifford(num_qubits)
        rand_circ = rand_cliff.to_circuit()
        inv_circ = rand_cliff.adjoint().to_circuit()
        new_circ = base_circuit.copy()
        new_circ = new_circ.compose(rand_circ)
        new_circ = new_circ.compose(inv_circ)
        result.append(new_circ)
    return result
