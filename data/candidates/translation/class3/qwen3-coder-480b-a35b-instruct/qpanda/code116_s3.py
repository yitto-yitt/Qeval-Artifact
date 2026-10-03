# EVAL_META: task_id=116, framework=qpanda, class=3
from pyqpanda3.core import *
import numpy as np

def synthesize_evolution_gate(pauli_string, time):
    # Create quantum program and machine
    prog = QProg()
    qvm = CPUQVM()
    qvm.init_qvm()
    
    # Get number of qubits based on length of pauli string
    n_qubits = len(pauli_string)
    qubits = qvm.qAlloc_many(n_qubits)
    
    # Build Hamiltonian from Pauli string
    hamiltonian = PauliOperator()
    
    # Convert the Pauli string to the appropriate form for pyQPanda
    coeff = 1.0
    term_str = ""
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char != 'I':
            term_str += f"{pauli_char}{i} "
    
    if term_str.strip():
        hamiltonian = PauliOperator({term_str.strip(): coeff})
    else:
        # If all identities, just return empty circuit
        pass
    
    # Perform time evolution: exp(-i * H * t)
    # Using Trotter evolution
    if term_str.strip():
        trotter = create_trotter_circuit(hamiltonian, -time, 2)  # 2nd order Trotter
        prog << trotter
    
    return prog
