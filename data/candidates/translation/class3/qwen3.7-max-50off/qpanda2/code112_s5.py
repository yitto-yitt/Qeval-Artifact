# EVAL_META: task_id=112, framework=qpanda2, class=3
import numpy as np
from pyqpanda import *

machine = CPUQVM()
machine.init()
qubits = machine.qAlloc_many(128)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        s = str(pauli_string)
        sign = 1.0
        if s.startswith('-'):
            sign = -1.0
            s = s[1:]
        elif s.startswith('+'):
            s = s[1:]
        if s.startswith('i'):
            s = s[1:]
        s = s.upper()
            
        non_id = [(i, p) for i, p in enumerate(s) if p != 'I']
        
        if not non_id:
            continue
            
        for _ in range(int(reps)):
            t_slice = (time * sign) / reps
            
            for i, p in non_id:
                if p == 'X':
                    prog << H(qubits[i])
                elif p == 'Y':
                    prog << RX(qubits[i], -np.pi/2)
                    
            if len(non_id) > 1:
                for j in range(len(non_id) - 1):
                    ctrl = non_id[j][0]
                    tgt = non_id[j+1][0]
                    prog << CNOT(qubits[ctrl], qubits[tgt])
                    
            target_idx = non_id[-1][0]
            prog << RZ(qubits[target_idx], 2 * t_slice)
            
            if len(non_id) > 1:
                for j in range(len(non_id) - 2, -1, -1):
                    ctrl = non_id[j][0]
                    tgt = non_id[j+1][0]
                    prog << CNOT(qubits[ctrl], qubits[tgt])
                    
            for i, p in non_id:
                if p == 'X':
                    prog << H(qubits[i])
                elif p == 'Y':
                    prog << RX(qubits[i], np.pi/2)
                    
    return prog

machine.finalize()
