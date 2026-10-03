# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

# Initialize CPUQVM and allocate qubits at global scope
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(100)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    active_qubits_and_paulis = []
    for i, char in enumerate(pauli_string):
        if char != 'I':
            qubit_idx = n - 1 - i
            active_qubits_and_paulis.append((qubit_idx, char))
            
    active_qubits_and_paulis.sort(key=lambda x: x[0])
    
    prog = pq.QCircuit()
    
    if not active_qubits_and_paulis:
        return prog
        
    for q_idx, char in active_qubits_and_paulis:
        if char == 'X':
            prog << pq.H(q[q_idx])
        elif char == 'Y':
            prog << pq.RX(q[q_idx], np.pi / 2)
            
    num_active = len(active_qubits_and_paulis)
    for i in range(num_active - 1):
        ctrl = active_qubits_and_paulis[i][0]
        target = active_qubits_and_paulis[i+1][0]
        prog << pq.CNOT(q[ctrl], q[target])
        
    last_q_idx = active_qubits_and_paulis[-1][0]
    prog << pq.RZ(q[last_q_idx], 2 * time)
    
    for i in range(num_active - 2, -1, -1):
        ctrl = active_qubits_and_paulis[i][0]
        target = active_qubits_and_paulis[i+1][0]
        prog << pq.CNOT(q[ctrl], q[target])
        
    for q_idx, char in active_qubits_and_paulis:
        if char == 'X':
            prog << pq.H(q[q_idx])
        elif char == 'Y':
            prog << pq.RX(q[q_idx], -np.pi / 2)
            
    return prog

# Manual Cleanup
machine.finalize()
