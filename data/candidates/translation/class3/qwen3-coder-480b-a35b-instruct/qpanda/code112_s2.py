# EVAL_META: task_id=112, framework=qpanda, class=3
import pyqpanda3 as pq
from pyqpanda3 import *
import numpy as np

def create_product_formula_circuit(pauli_strings, times, order, reps):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(len(pauli_strings[0]))
    
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        # Create Hamiltonian based on Pauli string
        hamiltonian = []
        for i, pauli_op in enumerate(pauli_string):
            if pauli_op == 'X':
                hamiltonian.append([1.0, ['X', [i]]])
            elif pauli_op == 'Y':
                hamiltonian.append([1.0, ['Y', [i]]])
            elif pauli_op == 'Z':
                hamiltonian.append([1.0, ['Z', [i]]])
        
        # Apply Trotter evolution
        for rep in range(reps):
            for coeff_pauli in hamiltonian:
                coeff = coeff_pauli[0] * time / reps
                pauli_type = coeff_pauli[1][0]
                target_qubit = coeff_pauli[1][1][0]
                
                if pauli_type == 'X':
                    prog.insert(RX(qubits[target_qubit], -2 * coeff))
                elif pauli_type == 'Y':
                    prog.insert(RY(qubits[target_qubit], -2 * coeff))
                elif pauli_type == 'Z':
                    prog.insert(RZ(qubits[target_qubit], -2 * coeff))
    
    return prog
