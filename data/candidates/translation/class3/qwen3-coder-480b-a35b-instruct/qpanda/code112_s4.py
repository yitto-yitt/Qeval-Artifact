# EVAL_META: task_id=112, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(len(pauli_strings[0]))
    
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Hamiltonian terms
        pauli_terms = []
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op != 'I':
                coeff = 1.0
                if pauli_op == 'X':
                    pauli_terms.append((coeff, [(qubits[i], 'X')]))
                elif pauli_op == 'Y':
                    pauli_terms.append((coeff, [(qubits[i], 'Y')]))
                elif pauli_op == 'Z':
                    pauli_terms.append((coeff, [(qubits[i], 'Z')]))
        
        # Apply Trotter evolution for the specified time
        for rep in range(reps):
            for coeff, term in pauli_terms:
                evolved_time = time / reps
                if len(term) == 1:
                    qubit_idx, pauli_type = term[0]
                    if pauli_type == 'X':
                        prog << RX(qubit_idx, 2 * coeff * evolved_time)
                    elif pauli_type == 'Y':
                        prog << RY(qubit_idx, 2 * coeff * evolved_time)
                    elif pauli_type == 'Z':
                        prog << RZ(qubit_idx, 2 * coeff * evolved_time)
    
    return prog
