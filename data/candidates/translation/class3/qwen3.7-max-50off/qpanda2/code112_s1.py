# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        non_id_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
        if not non_id_indices:
            continue
            
        dt = time / reps
        
        for _ in range(reps):
            # Basis change
            for i in non_id_indices:
                p = pauli_string[i]
                if p == 'X':
                    prog << pq.H(qubits[i])
                elif p == 'Y':
                    prog << pq.RX(qubits[i], np.pi / 2)
                    
            # CNOT cascade
            for j in range(len(non_id_indices) - 1):
                prog << pq.CNOT(qubits[non_id_indices[j]], qubits[non_id_indices[j+1]])
                
            # Rz
            last_q = non_id_indices[-1]
            prog << pq.RZ(qubits[last_q], 2 * dt)
            
            # Reverse CNOT cascade
            for j in range(len(non_id_indices) - 2, -1, -1):
                prog << pq.CNOT(qubits[non_id_indices[j]], qubits[non_id_indices[j+1]])
                
            # Reverse basis change
            for i in non_id_indices:
                p = pauli_string[i]
                if p == 'X':
                    prog << pq.H(qubits[i])
                elif p == 'Y':
                    prog << pq.RX(qubits[i], -np.pi / 2)
                    
    return prog

machine.finalize()
