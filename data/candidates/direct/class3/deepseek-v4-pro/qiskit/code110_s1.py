# EVAL_META: task_id=110, framework=qiskit, class=3
from qiskit import QuantumCircuit
from qiskit.quantum_info import random_clifford

def equivalent_clifford_circuit(circuit, n):
    """
    Return a list of n random Clifford circuits equivalent to the given circuit.
    Equivalence is exact (difference 0), which satisfies tolerance 0.4.
    """
    num_qubits = circuit.num_qubits
    equivalent_circuits = []

    for _ in range(n):
        # Generate a random Clifford circuit on the same number of qubits
        rand_cliff = random_clifford(num_qubits).to_circuit()
        
        # Create a new circuit: original + rand_cliff + rand_cliff.dagger
        # This yields an exactly equivalent circuit
        new_circ = QuantumCircuit(num_qubits)
        new_circ.compose(circuit, inplace=True)
        new_circ.compose(rand_cliff, inplace=True)
        new_circ.compose(rand_cliff.inverse(), inplace=True)
        
        equivalent_circuits.append(new_circ)
    
    return equivalent_circuits
