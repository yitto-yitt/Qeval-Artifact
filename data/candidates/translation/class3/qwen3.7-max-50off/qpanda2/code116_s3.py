# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(100)

def synthesize_evolution_gate(pauli_string, time):
    circ = pq.QCircuit()
    
    # Basis change to diagonalize the Pauli string
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circ << pq.H(qubits[i])
        elif p == 'Y':
            circ << pq.RX(qubits[i], np.pi / 2)
            
    non_id_indices = [i for i, p in enumerate(pauli_string) if p != 'I']
    
    # Parity computation, phase application, and uncomputation
    if len(non_id_indices) > 0:
        for m in range(len(non_id_indices) - 1):
            circ << pq.CNOT(qubits[non_id_indices[m]], qubits[non_id_indices[m+1]])
            
        # Rz(theta) = exp(-i * theta/2 * Z). We want exp(-i * time * Z), so theta = 2 * time
        circ << pq.RZ(qubits[non_id_indices[-1]], 2 * time)
        
        for m in range(len(non_id_indices) - 2, -1, -1):
            circ << pq.CNOT(qubits[non_id_indices[m]], qubits[non_id_indices[m+1]])
            
    # Undo basis change
    for i, p in enumerate(pauli_string):
        if p == 'X':
            circ << pq.H(qubits[i])
        elif p == 'Y':
            circ << pq.RX(qubits[i], -np.pi / 2)
            
    return circ

machine.finalize()
