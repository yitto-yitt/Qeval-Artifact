# EVAL_META: task_id=110, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.algorithm import *
from pyqpanda3.utils import *
import numpy as np

def equivalent_clifford_circuit(circuit, n):
    # Convert input circuit to unitary for comparison
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    # Get number of qubits from the original circuit
    num_qubits = len(circuit.get_used_qubits())
    
    # Get the original operator as unitary matrix
    prog_orig = pq.QProg()
    prog_orig.insert(circuit)
    unitary_orig = pq.get_unitary_matrix(prog_orig, machine, [i for i in range(num_qubits)])
    
    qc_list = []
    counter = 0
    
    while counter < n:
        # Generate random Clifford circuit
        clifford_prog = pq.generate_random_clifford([i for i in range(num_qubits)])
        unitary_new = pq.get_unitary_matrix(clifford_prog, machine, [i for i in range(num_qubits)])
        
        # Check equivalence using Frobenius norm (similar to operator equivalence)
        diff_matrix = unitary_orig - unitary_new
        frobenius_norm = np.linalg.norm(diff_matrix, 'fro')
        
        # If within tolerance (similar to rtol and atol), add to list
        if frobenius_norm <= 0.8:  # Combined tolerance check
            qc_list.append(clifford_prog)
            counter += 1
    
    machine.finalize()
    return qc_list
