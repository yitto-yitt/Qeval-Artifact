# EVAL_META: task_id=116, framework=qpanda, class=3
import pyqpanda3.core as pq
import math

def synthesize_evolution_gate(pauli_string, time):
    try:
        pq.init_quantum_machine(pq.QMachineType.CPU)
    except Exception:
        pass
    
    n = len(pauli_string)
    qubits = pq.qAlloc_many(n)
    
    circuit = pq.QCircuit()
    
    # Identify active qubits
    # Qiskit's qubit 0 is the rightmost character of pauli_string
    active_qubits = []
    for i in range(n):
        op = pauli_string[n - 1 - i]
        if op != 'I':
            active_qubits.append((i, op))
            
    if not active_qubits:
        return circuit
        
    # Step 1: Basis change to Z
    for i, op in active_qubits:
        if op == 'X':
            circuit << pq.H(qubits[i])
        elif op == 'Y':
            circuit << pq.RX(qubits[i], -math.pi / 2)
            
    # Step 2: CNOT chain
    for j in range(len(active_qubits) - 1):
        ctrl = active_qubits[j][0]
        target = active_qubits[j+1][0]
        circuit << pq.CNOT(qubits[ctrl], qubits[target])
        
    # Step 3: RZ rotation
    target_qubit = active_qubits[-1][0]
    circuit << pq.RZ(qubits[target_qubit], 2 * time)
    
    # Step 4: CNOT chain reverse
    for j in range(len(active_qubits) - 2, -1, -1):
        ctrl = active_qubits[j][0]
        target = active_qubits[j+1][0]
        circuit << pq.CNOT(qubits[ctrl], qubits[target])
        
    # Step 5: Basis change reverse
    for i, op in active_qubits:
        if op == 'X':
            circuit << pq.H(qubits[i])
        elif op == 'Y':
            circuit << pq.RX(qubits[i], math.pi / 2)
            
    return circuit
