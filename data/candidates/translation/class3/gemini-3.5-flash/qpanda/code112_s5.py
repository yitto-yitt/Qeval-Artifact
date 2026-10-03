# EVAL_META: task_id=112, framework=qpanda, class=3
import math
from pyqpanda3.core import CPUQVM, QProg, H, RX, RZ, CNOT

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(num_qubits)
    
    prog = QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        dt = time / reps
        for _ in range(reps):
            active_qubits = []
            pauli_ops = []
            for i in range(num_qubits):
                op = pauli_string[num_qubits - 1 - i]
                if op != 'I':
                    active_qubits.append(q[i])
                    pauli_ops.append(op)
            
            if len(active_qubits) == 0:
                continue
                
            # Step 1: Basis change
            for q_idx, op in zip(active_qubits, pauli_ops):
                if op == 'X':
                    prog.insert(H(q_idx))
                elif op == 'Y':
                    prog.insert(RX(q_idx, -math.pi / 2))
            
            # Step 2: CNOT ladder
            for j in range(len(active_qubits) - 1):
                prog.insert(CNOT(active_qubits[j], active_qubits[j+1]))
                
            # Step 3: RZ rotation
            prog.insert(RZ(active_qubits[-1], 2 * dt))
            
            # Step 4: Uncompute CNOT ladder
            for j in range(len(active_qubits) - 2, -1, -1):
                prog.insert(CNOT(active_qubits[j], active_qubits[j+1]))
                
            # Step 5: Uncompute basis change
            for q_idx, op in zip(active_qubits, pauli_ops):
                if op == 'X':
                    prog.insert(H(q_idx))
                elif op == 'Y':
                    prog.insert(RX(q_idx, math.pi / 2))
                    
    return prog
