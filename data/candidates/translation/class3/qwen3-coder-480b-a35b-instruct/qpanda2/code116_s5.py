# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def synthesize_evolution_gate(pauli_string, time):
    # Count number of qubits needed
    n_qubits = len(pauli_string)
    
    # Create quantum program
    prog = pq.QProg()
    
    # Allocate qubits for this specific program (we'll use the first n_qubits)
    qubits_local = qubits[:n_qubits]
    
    # Map Pauli string to corresponding gates
    pauli_ops = []
    for i, pauli_char in enumerate(pauli_string):
        if pauli_char == 'X':
            # For X: exp(-i * t * X/2) = RZ(π/2) * RX(t) * RZ(-π/2)
            prog << pq.RX(qubits_local[i], -time)
        elif pauli_char == 'Y':
            # For Y: exp(-i * t * Y/2) = RX(t)
            prog << pq.RY(qubits_local[i], -time)
        elif pauli_char == 'Z':
            # For Z: exp(-i * t * Z/2) = RZ(t)
            prog << pq.RZ(qubits_local[i], -time)
        elif pauli_char == 'I':
            # Identity does nothing
            continue
    
    return prog

machine.finalize()
