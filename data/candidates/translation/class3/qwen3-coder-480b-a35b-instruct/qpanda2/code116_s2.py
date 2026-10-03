# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()

def synthesize_evolution_gate(pauli_string, time):
    # Count number of qubits needed
    n_qubits = len(pauli_string)
    
    # Allocate qubits
    qubits = machine.qAlloc_many(n_qubits)
    
    # Create quantum program
    prog = pq.QProg()
    
    # Process each Pauli operator in the string
    for i, pauli_op in enumerate(pauli_string):
        if pauli_op == 'X':
            # For X: exp(-i * time * X) = RZ(pi/2) * RX(2*time) * RZ(-pi/2)
            prog << pq.RZ(qubits[i], np.pi / 2) << pq.RX(qubits[i], 2 * time) << pq.RZ(qubits[i], -np.pi / 2)
        elif pauli_op == 'Y':
            # For Y: exp(-i * time * Y) = RX(2*time)
            prog << pq.RX(qubits[i], 2 * time)
        elif pauli_op == 'Z':
            # For Z: exp(-i * time * Z) = RZ(2*time)
            prog << pq.RZ(qubits[i], 2 * time)
        # If 'I', do nothing
    
    # For identity part, we don't need to add any gates
    # The evolution is implemented by rotating each non-identity Pauli term
    
    return prog

machine.finalize()
