# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = []

def get_qubits(n):
    if len(_global_qubits) < n:
        _global_qubits.extend(machine.qAlloc_many(n - len(_global_qubits)))
    return _global_qubits[:n]

def pauli_evolution_circuit(qubits, pauli_string, time):
    circ = pq.QCircuit()
    non_id_qubits = []
    for i, p in enumerate(pauli_string):
        if p.upper() != 'I':
            non_id_qubits.append(i)
            
    if not non_id_qubits:
        return circ

    for i in non_id_qubits:
        p = pauli_string[i].upper()
        if p == 'X':
            circ << pq.H(qubits[i])
        elif p == 'Y':
            circ << pq.RX(qubits[i], np.pi / 2)
            
    for i in range(len(non_id_qubits) - 1):
        circ << pq.CNOT(qubits[non_id_qubits[i]], qubits[non_id_qubits[i+1]])
        
    last_q = non_id_qubits[-1]
    circ << pq.RZ(qubits[last_q], 2 * time)
    
    for i in range(len(non_id_qubits) - 2, -1, -1):
        circ << pq.CNOT(qubits[non_id_qubits[i]], qubits[non_id_qubits[i+1]])
        
    for i in non_id_qubits:
        p = pauli_string[i].upper()
        if p == 'X':
            circ << pq.H(qubits[i])
        elif p == 'Y':
            circ << pq.RX(qubits[i], -np.pi / 2)
            
    return circ

def create_product_formula_circuit(pauli_strings, times, order, reps):
    n = len(pauli_strings[0])
    qubits = get_qubits(n)
    
    qc = pq.QCircuit()
    
    for pauli_string, time in zip(pauli_strings, times):
        p_str = pauli_string[::-1]
        dt = time / reps
        for _ in range(reps):
            circ = pauli_evolution_circuit(qubits, p_str, dt)
            qc << circ
            
    return qc

machine.finalize()
