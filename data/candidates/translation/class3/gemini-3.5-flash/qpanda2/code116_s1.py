# EVAL_META: task_id=116, framework=qpanda2, class=3
from pyqpanda import *
import numpy as np

# Global QVM initialization
machine = CPUQVM()
machine.init_qvm()
global_qubits = machine.qAlloc_many(30)

def synthesize_evolution_gate(pauli_string, time):
    n = len(pauli_string)
    active = []
    for i in range(n):
        op = pauli_string[i]
        if op != 'I':
            q_idx = n - 1 - i
            active.append((q_idx, op))
            
    # Sort by qubit index ascending
    active.sort(key=lambda x: x[0])
    
    circuit = QCircuit()
    if not active:
        return circuit
        
    active_qubits = [global_qubits[x[0]] for x in active]
    active_ops = [x[1] for x in active]
    
    # Step 1: Basis change
    for q, op in zip(active_qubits, active_ops):
        if op == 'X':
            circuit << H(q)
        elif op == 'Y':
            circuit << RX(q, np.pi / 2)
            
    # Step 2: CNOT cascade
    n_active = len(active_qubits)
    for j in range(n_active - 1):
        circuit << CNOT(active_qubits[j], active_qubits[j+1])
        
    # Step 3: RZ rotation
    target_q = active_qubits[-1]
    circuit << RZ(target_q, 2 * time)
    
    # Step 4: Uncompute CNOT cascade
    for j in range(n_active - 2, -1, -1):
        circuit << CNOT(active_qubits[j], active_qubits[j+1])
        
    # Step 5: Uncompute basis change
    for q, op in zip(active_qubits, active_ops):
        if op == 'X':
            circuit << H(q)
        elif op == 'Y':
            circuit << RX(q, -np.pi / 2)
            
    return circuit

if __name__ == '__main__':
    machine.finalize()
