# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = pq.QProg()
    
    for pauli_string, time in zip(pauli_strings, times):
        ops = pauli_string[::-1]
        active_qubits = []
        active_ops = []
        for i, op in enumerate(ops):
            if op != 'I':
                active_qubits.append(qubits[i])
                active_ops.append(op)
                
        if not active_qubits:
            continue
            
        theta = time / reps
        
        for _ in range(reps):
            for q, op in zip(active_qubits, active_ops):
                if op == 'X':
                    prog << pq.H(q)
                elif op == 'Y':
                    prog << pq.RX(q, np.pi / 2)
                    
            for i in range(len(active_qubits) - 1):
                prog << pq.CNOT(active_qubits[i], active_qubits[i+1])
                
            prog << pq.RZ(active_qubits[-1], 2 * theta)
            
            for i in reversed(range(len(active_qubits) - 1)):
                prog << pq.CNOT(active_qubits[i], active_qubits[i+1])
                
            for q, op in zip(active_qubits, active_ops):
                if op == 'X':
                    prog << pq.H(q)
                elif op == 'Y':
                    prog << pq.RX(q, -np.pi / 2)
                    
    return prog

machine.finalize()
