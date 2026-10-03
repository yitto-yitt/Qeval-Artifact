# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qubits = machine.qAlloc_many(len(pauli_strings[0]))
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Hamiltonian terms
        hamiltonian_terms = []
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'X':
                hamiltonian_terms.append((pq.PauliOperator({qubits[i]: 'X'}), 1.0))
            elif pauli_op == 'Y':
                hamiltonian_terms.append((pq.PauliOperator({qubits[i]: 'Y'}), 1.0))
            elif pauli_op == 'Z':
                hamiltonian_terms.append((pq.PauliOperator({qubits[i]: 'Z'}), 1.0))
        
        # Apply Trotter evolution for each term
        for _ in range(reps):
            for pauli_op, coeff in hamiltonian_terms:
                # Scale time by reps for proper decomposition
                scaled_time = time / reps
                prog << pq.apply_trotter_evolution(pauli_op, scaled_time, 1)
    
    return prog, qubits

def finalize():
    machine.finalize()
