# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def and_gate(a: int, b: int) -> dict:
    # Create a quantum circuit with 9 qubits and 3 classical bits
    qc = QuantumCircuit(9, 3)
    
    # Convert integer inputs to 3-bit binary representation [MSB, ..., LSB]
    a_bits = [int(x) for x in format(a, '03b')]
    b_bits = [int(x) for x in format(b, '03b')]
    
    # Initialize qubits for 'a' (qubits 0, 1, 2 correspond to LSB to MSB)
    if a_bits[2] == 1: qc.x(0) # a0 (LSB)
    if a_bits[1] == 1: qc.x(1) # a1
    if a_bits[0] == 1: qc.x(2) # a2 (MSB)
        
    # Initialize qubits for 'b' (qubits 3, 4, 5 correspond to LSB to MSB)
    if b_bits[2] == 1: qc.x(3) # b0 (LSB)
    if b_bits[1] == 1: qc.x(4) # b1
    if b_bits[0] == 1: qc.x(5) # b2 (MSB)
        
    # Perform bitwise AND using Toffoli gates
    qc.ccx(0, 3, 6) # c0 = a0 & b0
    qc.ccx(1, 4, 7) # c1 = a1 & b1
    qc.ccx(2, 5, 8) # c2 = a2 & b2
    
    # Measure output qubits 6, 7, 8 to classical bits 0, 1, 2
    qc.measure(6, 0)
    qc.measure(7, 1)
    qc.measure(8, 2)
    
    # Simulate the circuit
    backend = AerSimulator()
    t_qc = transpile(qc, backend)
    result = backend.run(t_qc, shots=1024).result()
    counts = result.get_counts()
    
    # Normalize to get the probability distribution
    total_shots = sum(counts.values())
    prob_dist = {k: v / total_shots for k, v in counts.items()}
    
    return prob_dist
