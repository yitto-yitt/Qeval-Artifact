# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(100)

def synthesize_evolution_gate(pauli_string, time):
    n_qubits = len(pauli_string)
    qubits = [global_qubits[i] for i in range(n_qubits)]
    
    circuit = pq.QCircuit()
    
    active_qubits = []
    active_paulis = []
    for i in range(n_qubits):
        op = pauli_string[n_qubits - 1 - i]
        if op != 'I':
            active_qubits.append(qubits[i])
            active_paulis.append(op)
            
    if not active_qubits:
        return circuit
        
    # Step 1: Basis change
    for q, op in zip(active_qubits, active_paulis):
        if op == 'X':
            circuit << pq.H(q)
        elif op == 'Y':
            circuit << pq.RX(q, -np.pi / 2)
            
    # Step 2: CNOT chain
    for i in range(len(active_qubits) - 1):
        circuit << pq.CNOT(active_qubits[i], active_qubits[i+1])
        
    # Step 3: RZ rotation
    circuit << pq.RZ(active_qubits[-1], 2 * time)
    
    # Step 4: Reverse CNOT chain
    for i in range(len(active_qubits) - 2, -1, -1):
        circuit << pq.CNOT(active_qubits[i], active_qubits[i+1])
        
    # Step 5: Reverse basis change
    for q, op in zip(active_qubits, active_paulis):
        if op == 'X':
            circuit << pq.H(q)
        elif op == 'Y':
            circuit << pq.RX(q, np.pi / 2)
            
    return circuit

# Manual Cleanup
machine.finalize()
