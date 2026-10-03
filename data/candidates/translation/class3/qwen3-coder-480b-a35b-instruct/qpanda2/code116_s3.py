# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

machine = pq.CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(10)

def synthesize_evolution_gate(pauli_string, time):
    # Count number of qubits needed based on pauli_string length
    n_qubits = len(pauli_string)
    
    # Create quantum program and circuit
    prog = pq.QProg()
    circuit = pq.QCircuit()
    
    # Map Pauli string to corresponding gates
    for i, pauli_op in enumerate(pauli_string):
        if pauli_op == 'X':
            # For X rotation: exp(-i * time * X/2) = R_X(-time)
            circuit.insert(pq.RX(qubits[i], -time))
        elif pauli_op == 'Y':
            # For Y rotation: exp(-i * time * Y/2) = R_Y(-time)
            circuit.insert(pq.RY(qubits[i], -time))
        elif pauli_op == 'Z':
            # For Z rotation: exp(-i * time * Z/2) = R_Z(-time)
            circuit.insert(pq.RZ(qubits[i], -time))
        # If 'I', do nothing
    
    prog.insert(circuit)
    return prog

# Manual cleanup
machine.finalize()
