# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    if not pauli_strings:
        return QProg()
        
    N = len(pauli_strings[0])
    try:
        init_quantum_machine(0) # QMachineType.CPU
    except:
        pass
    qubits = qAlloc_many(N)
    
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        active_qubits = []
        for idx, char in enumerate(pauli_string):
            if char != 'I':
                active_qubits.append(N - 1 - idx)
        
        active_qubits.sort()
        
        if len(active_qubits) > 0:
            target_qubit = active_qubits[0]
            for _ in range(reps):
                # Forward basis change
                for idx, char in enumerate(pauli_string):
                    q_idx = N - 1 - idx
                    if char == 'X':
                        prog << H(qubits[q_idx])
                    elif char == 'Y':
                        prog << RX(qubits[q_idx], math.pi / 2)
                
                # Forward CNOTs
                for j in range(len(active_qubits) - 1, 0, -1):
                    prog << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j-1]])
                
                # RZ
                angle = 2.0 * time / reps
                prog << RZ(qubits[target_qubit], angle)
                
                # Backward CNOTs
                for j in range(1, len(active_qubits)):
                    prog << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j-1]])
                
                # Backward basis change
                for idx, char in enumerate(pauli_string):
                    q_idx = N - 1 - idx
                    if char == 'X':
                        prog << H(qubits[q_idx])
                    elif char == 'Y':
                        prog << RX(qubits[q_idx], -math.pi / 2)
                        
    return prog
