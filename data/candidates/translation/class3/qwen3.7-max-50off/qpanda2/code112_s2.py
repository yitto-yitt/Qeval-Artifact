# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init()
qubits = machine.qAlloc_many(32)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    num_qubits = len(pauli_strings[0])
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        reversed_pauli = pauli_string[::-1]
        
        for _ in range(reps):
            theta = time / reps
            
            for i, p in enumerate(reversed_pauli):
                if p == 'X':
                    prog << pq.H(qubits[i])
                elif p == 'Y':
                    prog << pq.RX(qubits[i], np.pi / 2)
                    
            active_qubits = [i for i, p in enumerate(reversed_pauli) if p != 'I']
            if len(active_qubits) > 1:
                for i in range(len(active_qubits) - 1):
                    prog << pq.CNOT(qubits[active_qubits[i]], qubits[active_qubits[i+1]])
                    
                prog << pq.RZ(qubits[active_qubits[-1]], 2 * theta)
                
                for i in range(len(active_qubits) - 2, -1, -1):
                    prog << pq.CNOT(qubits[active_qubits[i]], qubits[active_qubits[i+1]])
            elif len(active_qubits) == 1:
                prog << pq.RZ(qubits[active_qubits[0]], 2 * theta)
                
            for i, p in enumerate(reversed_pauli):
                if p == 'X':
                    prog << pq.H(qubits[i])
                elif p == 'Y':
                    prog << pq.RX(qubits[i], -np.pi / 2)
                    
    return prog

machine.finalize()
