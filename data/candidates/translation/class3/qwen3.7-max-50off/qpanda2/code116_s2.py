# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(32)
c = machine.cAlloc_many(32)

def synthesize_evolution_gate(pauli_string, time):
    N = len(pauli_string)
    qc = pq.QCircuit()
    
    active_qubits = []
    for i, p in enumerate(pauli_string):
        if p != 'I':
            q_idx = N - 1 - i
            active_qubits.append((q_idx, p))
            
    if not active_qubits:
        return qc

    for q_idx, p in active_qubits:
        if p == 'X':
            qc << pq.H(q[q_idx])
        elif p == 'Y':
            qc << pq.RX(q[q_idx], np.pi / 2)
            
    if len(active_qubits) > 1:
        for i in range(len(active_qubits) - 1):
            ctrl = active_qubits[i][0]
            targ = active_qubits[i+1][0]
            qc << pq.CNOT(q[ctrl], q[targ])
            
    last_q = active_qubits[-1][0]
    qc << pq.RZ(q[last_q], 2 * time)
    
    if len(active_qubits) > 1:
        for i in range(len(active_qubits) - 2, -1, -1):
            ctrl = active_qubits[i][0]
            targ = active_qubits[i+1][0]
            qc << pq.CNOT(q[ctrl], q[targ])
            
    for q_idx, p in active_qubits:
        if p == 'X':
            qc << pq.H(q[q_idx])
        elif p == 'Y':
            qc << pq.RX(q[q_idx], -np.pi / 2)
            
    return qc

machine.finalize()
