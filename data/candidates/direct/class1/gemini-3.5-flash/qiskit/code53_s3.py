# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def xor_gate(a: int, b: int) -> dict:
    # We use 16 qubits: 8 for register A (0-7), 8 for register B (8-15)
    # Register B will store the XOR result
    qc = QuantumCircuit(16, 8)
    
    # Initialize register A with the bits of 'a'
    for i in range(8):
        bit_a = (a >> i) & 1
        if bit_a:
            qc.x(i)
            
    # Initialize register B with the bits of 'b'
    for i in range(8):
        bit_b = (b >> i) & 1
        if bit_b:
            qc.x(i + 8)
            
    # Perform XOR using CNOT gates from A to B
    for i in range(8):
        qc.cx(i, i + 8)
        
    # Measure register B into the 8 classical bits
    for i in range(8):
        qc.measure(i + 8, i)
        
    # Simulate the circuit
    backend = AerSimulator()
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=1024).result()
    counts = result.get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    prob_dist = {state: count / total_shots for state, count in counts.items()}
    
    return prob_dist
