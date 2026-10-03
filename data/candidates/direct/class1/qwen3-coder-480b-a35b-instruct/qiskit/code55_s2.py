# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    # Convert input integers to binary strings
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Create quantum circuit with 3 input qubits for a, 3 for b, and 3 for output
    qr = QuantumRegister(9)  # 3 for a, 3 for b, 3 for result
    cr = ClassicalRegister(3)  # 3 bits for output
    qc = QuantumCircuit(qr, cr)
    
    # Initialize input qubits based on a and b
    for i in range(3):
        if a_bin[i] == '1':
            qc.x(i)  # Apply X gate to set qubit to |1>
        if b_bin[i] == '1':
            qc.x(i + 3)  # Apply X gate to set qubit to |1>
    
    # Perform OR operation using CNOT and CCNOT gates
    # For each bit position, compute OR: (a_i OR b_i) = NOT(NOT a_i AND NOT b_i) XOR 1
    # Or more directly: OR can be computed as NOT((NOT a_i) AND (NOT b_i))
    # But we'll use the fact that OR = A + B - AB in boolean algebra
    # Using ancilla-free approach: OR of two bits can be computed by flipping target if at least one control is 1
    
    # We'll use the fact that OR can be implemented by flipping the output if both inputs are 0
    for i in range(3):
        # Copy a_i to result_i
        qc.cx(i, i+6)
        # Then apply logic to ensure OR behavior
        qc.x(i)     # Flip a_i
        qc.x(i+3)   # Flip b_i
        qc.ccx(i, i+3, i+6)  # Apply Toffoli: if both flipped are 1 (meaning original were 0), flip result
        qc.x(i)     # Flip a_i back
        qc.x(i+3)   # Flip b_i back
        qc.x(i+6)   # Final flip to get correct OR result
    
    # Measure the result qubits
    qc.measure([6, 7, 8], [0, 1, 2])
    
    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts()
    
    # Normalize counts to probabilities
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
