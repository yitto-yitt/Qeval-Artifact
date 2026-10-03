# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    num_qubits = len(pauli_strings[0])
    
    for pauli_string, time in zip(pauli_strings, times):
        for _ in range(reps):
            reversed_string = pauli_string[::-1]
            active_qubits = []
            for i in range(num_qubits):
                if reversed_string[i] != 'I':
                    active_qubits.append(i)
            
            if not active_qubits:
                continue
            
            # Basis change before
            for i in active_qubits:
                op = reversed_string[i]
                if op == 'X':
                    prog << H(q[i])
                elif op == 'Y':
                    prog << RX(q[i], np.pi / 2)
            
            # CNOT cascade
            for j in range(len(active_qubits) - 1):
                prog << CNOT(q[active_qubits[j]], q[active_qubits[j+1]])
            
            # RZ rotation
            target_qubit = active_qubits[-1]
            prog << RZ(q[target_qubit], 2.0 * time / reps)
            
            # CNOT cascade inverse
            for j in range(len(active_qubits) - 2, -1, -1):
                prog << CNOT(q[active_qubits[j]], q[active_qubits[j+1]])
                
            # Basis change after
            for i in active_qubits:
                op = reversed_string[i]
                if op == 'X':
                    prog << H(q[i])
                elif op == 'Y':
                    prog << RX(q[i], -np.pi / 2)
                    
    return prog

machine.finalize()
