# EVAL_META: task_id=112, framework=qpanda2, class=3
import math
from pyqpanda import *

# Initialize global QVM
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(24)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    num_qubits = len(pauli_strings[0])
    qubits = global_qubits[:num_qubits]
    
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            t_step = time / reps
            
            # Extract active qubits and their operators
            active_qubits = []
            active_ops = []
            for idx, char in enumerate(pauli_string):
                if char != 'I':
                    q_idx = num_qubits - 1 - idx
                    active_qubits.append(q_idx)
                    active_ops.append(char)
            
            if not active_qubits:
                continue
                
            # Sort by qubit index ascending
            sorted_indices = sorted(range(len(active_qubits)), key=lambda k: active_qubits[k])
            active_qubits = [active_qubits[k] for k in sorted_indices]
            active_ops = [active_ops[k] for k in sorted_indices]
            
            # 1. Basis change
            for q_idx, op in zip(active_qubits, active_ops):
                if op == 'X':
                    prog << H(qubits[q_idx])
                elif op == 'Y':
                    prog << RX(qubits[q_idx], math.pi / 2)
            
            # 2. CNOT cascade
            for j in range(len(active_qubits) - 1):
                prog << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
                
            # 3. RZ rotation
            prog << RZ(qubits[active_qubits[-1]], 2 * t_step)
            
            # 4. Reverse CNOT cascade
            for j in range(len(active_qubits) - 2, -1, -1):
                prog << CNOT(qubits[active_qubits[j]], qubits[active_qubits[j+1]])
                
            # 5. Inverse basis change
            for q_idx, op in zip(active_qubits, active_ops):
                if op == 'X':
                    prog << H(qubits[q_idx])
                elif op == 'Y':
                    prog << RX(qubits[q_idx], -math.pi / 2)
                    
    return prog

machine.finalize()
