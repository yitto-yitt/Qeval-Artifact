# EVAL_META: task_id=112, framework=qpanda2, class=3
from pyqpanda import *
import atexit

# Initialize CPUQVM globally to prevent premature garbage collection
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

# Register cleanup
atexit.register(machine.finalize)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    N = len(pauli_strings[0])
    qubits = global_qubits[:N]
    
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        theta = time / reps
        
        for _ in range(reps):
            active_qubits = []
            ops = []
            for i in range(N):
                op = pauli_string[i]
                if op != 'I':
                    q_idx = N - 1 - i
                    active_qubits.append(qubits[q_idx])
                    ops.append(op)
            
            if not active_qubits:
                continue
                
            # Basis change to Z
            for q, op in zip(active_qubits, ops):
                if op == 'X':
                    prog << H(q)
                elif op == 'Y':
                    prog << RX(q, 3.141592653589793 / 2)
            
            # CNOT ladder
            for i in range(len(active_qubits) - 1):
                prog << CNOT(active_qubits[i], active_qubits[i+1])
                
            # RZ evolution
            prog << RZ(active_qubits[-1], 2 * theta)
            
            # Inverse CNOT ladder
            for i in range(len(active_qubits) - 2, -1, -1):
                prog << CNOT(active_qubits[i], active_qubits[i+1])
                
            # Inverse basis change
            for q, op in zip(active_qubits, ops):
                if op == 'X':
                    prog << H(q)
                elif op == 'Y':
                    prog << RX(q, -3.141592653589793 / 2)
                    
    return prog
