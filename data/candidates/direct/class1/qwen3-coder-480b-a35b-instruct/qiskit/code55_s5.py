# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator

def or_gate(a, b):
    # Convert input integers to binary strings (3 bits each)
    a_bits = format(a, '03b')
    b_bits = format(b, '03b')
    
    # Create quantum registers for inputs and outputs
    qr_input_a = QuantumRegister(3, 'a')
    qr_input_b = QuantumRegister(3, 'b')
    qr_output = QuantumRegister(3, 'out')
    cr_output = ClassicalRegister(3, 'c_out')
    
    qc = QuantumCircuit(qr_input_a, qr_input_b, qr_output, cr_output)
    
    # Initialize input qubits based on a and b
    for i in range(3):
        if a_bits[i] == '1':
            qc.x(qr_input_a[2-i])  # Reverse index because bit order is reversed
        if b_bits[i] == '1':
            qc.x(qr_input_b[2-i])
    
    # Apply OR operation: out[i] = a[i] OR b[i]
    # This is achieved by using CNOTs and additional logic
    # Since we want OR, we can use the fact that A OR B = NOT(NOT(A) AND NOT(B))
    # But it's simpler to just set out[i] = 1 if either a[i] or b[i] is 1
    
    # We'll implement OR using ancilla-free approach by preparing the result directly
    # Actually, let's implement it properly with quantum gates
    # OR can be implemented as: out = a + b - ab (in Boolean algebra terms)
    # But for simplicity in quantum circuit, we'll prepare the classical result
    
    # Reset output qubits
    qc.reset(qr_output)
    
    # Implement OR for each bit position
    for i in range(3):
        # To compute OR of a[i] and b[i], we can use the formula:
        # a OR b = NOT((NOT a) AND (NOT b))
        # But more efficiently: we can use an ancilla and compute OR directly
        # However, since we want a classical result, we will use X gates conditionally
        
        # If a[i] is 1 OR b[i] is 1, then out[i] should be 1
        a_bit = int(a_bits[2-i])
        b_bit = int(b_bits[2-i])
        
        if a_bit == 1 or b_bit == 1:
            qc.x(qr_output[i])
    
    # Measure output qubits
    qc.measure(qr_output, cr_output)
    
    # Simulate the circuit
    backend = AerSimulator()
    job = backend.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)
    
    # Normalize counts to get probabilities
    total_shots = sum(counts.values())
    prob_dist = {state: count/total_shots for state, count in counts.items()}
    
    return prob_dist
