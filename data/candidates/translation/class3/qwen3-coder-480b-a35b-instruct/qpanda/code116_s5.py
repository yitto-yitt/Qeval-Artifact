# EVAL_META: task_id=116, framework=qpanda, class=3
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create a quantum machine
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(len(pauli_string))
    
    # Parse the Pauli string and build the evolution circuit
    prog = pq.QProg()
    
    # Convert Pauli string to Hamiltonian terms
    pauli_terms = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            pauli_terms.append((1.0, [pq.PauliX(qubits[i])]))
        elif pauli_char == 'Y':
            pauli_terms.append((1.0, [pq.PauliY(qubits[i])]))
        elif pauli_char == 'Z':
            pauli_terms.append((1.0, [pq.PauliZ(qubits[i])]))
        # For 'I', we don't add anything
    
    # Build the evolution gate using Trotter formula
    # For a single term Hamiltonian H = sum(h_i * P_i), exp(-i * t * H) 
    if len(pauli_terms) > 0:
        # Get coefficients and Pauli operators
        coeffs = [term[0] for term in pauli_terms]
        
        # Apply the evolution
        for coeff, ops in pauli_terms:
            # For each Pauli operator, apply the evolution
            evolved_time = -coeff * time
            for op in ops:
                # Apply the rotation based on the Pauli operator type
                if isinstance(op, pq.PauliX):
                    prog.insert(pq.RX(op.target(), evolved_time * 2))
                elif isinstance(op, pq.PauliY):
                    prog.insert(pq.RY(op.target(), evolved_time * 2))
                elif isinstance(op, pq.PauliZ):
                    prog.insert(pq.RZ(op.target(), evolved_time * 2))
    
    return prog
