# EVAL_META: task_id=116, framework=qpanda2, class=3
import pyqpanda as pq
import numpy as np

# Global QVM initialization
machine = pq.CPUQVM()
machine.init_qvm()
q = machine.qAlloc_many(24)

def synthesize_evolution_gate(pauli_string, time):
    circuit = pq.QCircuit()
    n = len(pauli_string)
    
    active = []
    for i in range(n):
        char = pauli_string[i]
        if char != 'I':
            qubit_idx = n - 1 - i
            active.append((qubit_idx, char))
            
    # Sort active by qubit index
    active.sort(key=lambda x: x[0])
    
    if not active:
        return circuit
        
    # Basis change before
    for qubit_idx, char in active:
        if char == 'X':
            circuit << pq.H(q[qubit_idx])
        elif char == 'Y':
            circuit << pq.RX(q[qubit_idx], np.pi / 2)
            
    # CNOT cascade
    k = len(active)
    for j in range(k - 1):
        circuit << pq.CNOT(q[active[j][0]], q[active[j+1][0]])
        
    # RZ evolution
    circuit << pq.RZ(q[active[-1][0]], 2 * time)
    
    # CNOT cascade inverse
    for j in range(k - 2, -1, -1):
        circuit << pq.CNOT(q[active[j][0]], q[active[j+1][0]])
        
    # Basis change after
    for qubit_idx, char in active:
        if char == 'X':
            circuit << pq.H(q[qubit_idx])
        elif char == 'Y':
            circuit << pq.RX(q[qubit_idx], -np.pi / 2)
            
    return circuit

if __name__ == '__main__':
    machine.finalize()
