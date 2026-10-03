# EVAL_META: task_id=112, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qvm = pq.QVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(len(pauli_strings[0]))
    
    circuit = pq.QCircuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Convert Pauli string to Hamiltonian terms
        pauli_terms = []
        coeff_list = []
        
        # Create Hamiltonian based on Pauli string
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'I':
                continue
            elif pauli_op == 'X':
                pauli_str = "X" + str(i)
            elif pauli_op == 'Y':
                pauli_str = "Y" + str(i)
            elif pauli_op == 'Z':
                pauli_str = "Z" + str(i)
            
            pauli_terms.append(pauli_str)
            coeff_list.append(time)  # Using time as coefficient
        
        if len(pauli_terms) > 0:
            # Create Hamiltonian
            hamiltonian = pq.Hamiltonian(pauli_terms, coeff_list)
            
            # Trotter evolution - Lie-Trotter
            trotter_circuit = pq.trotter_evolution(
                hamiltonian,
                time,
                1,  # order (Lie-Trotter is order 1)
                reps
            )
            circuit.push_back(trotter_circuit)
    
    qvm.qFree_all(qubits)
    return circuit
