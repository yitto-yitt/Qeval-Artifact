# EVAL_META: task_id=112, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Determine number of qubits needed
    num_qubits = len(pauli_strings[0])
    qubits = qvm.qAlloc_many(num_qubits)
    
    # Create quantum program
    prog = pq.QProg()
    
    # Process each Pauli string with its corresponding time
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Hamiltonian terms
        pauli_terms = []
        
        # Build the Hamiltonian from Pauli string
        hamiltonian_str = ""
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char != 'I':
                if hamiltonian_str:
                    hamiltonian_str += " + "
                hamiltonian_str += f"{pauli_char}{i}"
        
        if hamiltonian_str:
            # Create Pauli operator based on the string
            pauli_list = []
            for i, pauli_char in enumerate(pauli_string):
                if pauli_char != 'I':
                    pauli_list.append((pauli_char, i))
            
            # Apply Trotter evolution
            for rep in range(reps):
                for pauli_char, idx in pauli_list:
                    if pauli_char == 'X':
                        prog << RX(qubits[idx], 2 * time / reps)
                    elif pauli_char == 'Y':
                        prog << RY(qubits[idx], 2 * time / reps)
                    elif pauli_char == 'Z':
                        prog << RZ(qubits[idx], 2 * time / reps)
    
    # Create a quantum circuit from the program
    # Since pyQPanda doesn't have a direct circuit class like Qiskit,
    # we return the program which contains the operations
    return prog
