# EVAL_META: task_id=116, framework=qpanda, class=3
import math
from pyqpanda3.core import CPUQVM, QProg, H, RX, RZ, CNOT

def synthesize_evolution_gate(pauli_string, time):
    # Initialize the virtual machine
    machine = CPUQVM()
    machine.init_qvm()
    
    n_qubits = len(pauli_string)
    qubits = machine.qAlloc_many(n_qubits)
    
    prog = QProg()
    
    # Identify active qubits and their corresponding Pauli operators
    paulis = []
    for i, char in enumerate(pauli_string):
        if char != 'I':
            q_idx = n_qubits - 1 - i
            paulis.append((q_idx, char))
            
    # Sort by qubit index to ensure consistent CNOT ordering
    paulis.sort(key=lambda x: x[0])
    
    if not paulis:
        # If all are identity, return empty program
        prog.machine = machine
        return prog
        
    # Step 1: Basis change before the CNOT cascade
    for q_idx, char in paulis:
        if char == 'X':
            prog << H(qubits[q_idx])
        elif char == 'Y':
            prog << RX(qubits[q_idx], math.pi / 2)
            
    # Step 2: Forward CNOT cascade
    k = len(paulis)
    for j in range(k - 1):
        prog << CNOT(qubits[paulis[j][0]], qubits[paulis[j+1][0]])
        
    # Step 3: RZ rotation on the last active qubit
    last_q_idx = paulis[-1][0]
    prog << RZ(qubits[last_q_idx], 2 * time)
    
    # Step 4: Backward CNOT cascade
    for j in range(k - 2, -1, -1):
        prog << CNOT(qubits[paulis[j][0]], qubits[paulis[j+1][0]])
        
    # Step 5: Basis change after the CNOT cascade
    for q_idx, char in paulis:
        if char == 'X':
            prog << H(qubits[q_idx])
        elif char == 'Y':
            prog << RX(qubits[q_idx], -math.pi / 2)
            
    # Keep the machine alive by attaching it to the program
    prog.machine = machine
    return prog
