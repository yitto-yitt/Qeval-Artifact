# EVAL_META: task_id=112, framework=qpanda2, class=3
import pyqpanda as pq
from pyqpanda import QProg, QCircuit, QGate
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def create_product_formula_circuit(pauli_strings, times, order, reps):
    prog = QProg()
    
    # Determine the number of qubits needed
    num_qubits = len(pauli_strings[0])
    local_qubits = qubits[:num_qubits]
    
    for pauli_string, time in zip(pauli_strings, times):
        # Create circuit for each Pauli string evolution
        circuit = QCircuit()
        
        # Process each position in the Pauli string
        for i, pauli_char in enumerate(pauli_string):
            if pauli_char == 'X':
                # For X rotation, we can use H - Z - H transformation
                circuit << pq.H(local_qubits[i]) << pq.RZ(local_qubits[i], -2 * time * reps) << pq.H(local_qubits[i])
            elif pauli_char == 'Y':
                # For Y rotation, we can use S - H - Z - H - S^dag transformation
                circuit << pq.S(local_qubits[i]).dagger() << pq.H(local_qubits[i]) << pq.RZ(local_qubits[i], -2 * time * reps) << pq.H(local_qubits[i]) << pq.S(local_qubits[i])
            elif pauli_char == 'Z':
                # For Z rotation directly apply RZ
                circuit << pq.RZ(local_qubits[i], -2 * time * reps)
            # If it's 'I', do nothing
        
        prog << circuit
    
    return prog

machine.finalize()
