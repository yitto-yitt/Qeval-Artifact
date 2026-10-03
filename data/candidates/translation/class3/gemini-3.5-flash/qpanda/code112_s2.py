# EVAL_META: task_id=112, framework=qpanda, class=3
import numpy as np
from pyqpanda3.core import *

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        theta = time / reps
        for _ in range(reps):
            active_qubits = []
            for i in range(num_qubits):
                op = pauli_string[num_qubits - 1 - i]
                if op != 'I':
                    active_qubits.append(i)
            
            if len(active_qubits) == 0:
                continue
            elif len(active_qubits) == 1:
                q_idx = active_qubits[0]
                op = pauli_string[num_qubits - 1 - q_idx]
                if op == 'X':
                    prog << H(q[q_idx])
                elif op == 'Y':
                    prog << RX(q[q_idx], np.pi / 2)
                
                prog << RZ(q[q_idx], 2 * theta)
                
                if op == 'X':
                    prog << H(q[q_idx])
                elif op == 'Y':
                    prog << RX(q[q_idx], -np.pi / 2)
            else:
                # Basis change
                for q_idx in active_qubits:
                    op = pauli_string[num_qubits - 1 - q_idx]
                    if op == 'X':
                        prog << H(q[q_idx])
                    elif op == 'Y':
                        prog << RX(q[q_idx], np.pi / 2)
                
                # CNOT chain
                for idx in range(len(active_qubits) - 1):
                    prog << CNOT(q[active_qubits[idx]], q[active_qubits[idx + 1]])
                
                # RZ on target
                target_q = active_qubits[-1]
                prog << RZ(q[target_q], 2 * theta)
                
                # Inverse CNOT chain
                for idx in reversed(range(len(active_qubits) - 1)):
                    prog << CNOT(q[active_qubits[idx]], q[active_qubits[idx + 1]])
                
                # Inverse basis change
                for q_idx in active_qubits:
                    op = pauli_string[num_qubits - 1 - q_idx]
                    if op == 'X':
                        prog << H(q[q_idx])
                    elif op == 'Y':
                        prog << RX(q[q_idx], -np.pi / 2)
                        
    return prog
