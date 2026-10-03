# EVAL_META: task_id=110, framework=qiskit, class=3

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Clifford, random_clifford
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import OptimizeCliffords


def equivalent_clifford_circuit(circuit, n):
    # Get the Clifford representation of the input circuit
    original_clifford = Clifford(circuit)
    
    # Optimize the original circuit to get a canonical form
    pass_manager = PassManager([OptimizeCliffords()])
    optimized_circuit = pass_manager.run(circuit)
    reference_clifford = Clifford(optimized_circuit)
    
    equivalent_circuits = []
    
    # Generate n equivalent circuits
    for _ in range(n):
        # Create a random clifford circuit on the same number of qubits
        num_qubits = circuit.num_qubits
        random_cliff = random_clifford(num_qubits)
        
        # Create the inverse of the random clifford
        random_cliff_inv = random_cliff.adjoint()
        
        # Compose: random_cliff_inv @ original_clifford @ random_cliff
        # This should be equivalent to the original up to clifford equivalence
        equivalent_cliff = random_cliff_inv.compose(reference_clifford).compose(random_cliff)
        
        # Convert back to circuit
        equiv_circuit = equivalent_cliff.to_circuit()
        equivalent_circuits.append(equiv_circuit)
    
    return equivalent_circuits
