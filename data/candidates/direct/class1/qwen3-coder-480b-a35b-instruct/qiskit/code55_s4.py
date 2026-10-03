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
    
    # Initialize input qubits based on the binary representation of a and b
    for i in range(3):
        if a_bits[i] == '1':
            qc.x(qr_input_a[2-i])  # Reverse index to match bit order
        if b_bits[i] == '1':
            qc.x(qr_input_b[2-i])  # Reverse index to match bit order
    
    # Perform OR operation using CNOT and CCNOT gates
    # For each bit position, compute OR: out_i = a_i OR b_i
    for i in range(3):
        # OR can be implemented as: A OR B = NOT(NOT(A) AND NOT(B))
        # But more efficiently: OR can be achieved with X gates and ancilla logic
        # Here we'll use the fact that OR is equivalent to: A + B - AB (in Boolean algebra)
        # We'll use ancilla qubits to compute AND then combine
        
        # Actually, let's implement OR directly: OR(a,b) = NOT(NAND(a,b)) but that needs extra qubit
        # Simpler approach: use the fact that OR(a,b) = A XOR B XOR (A AND B)
        
        # Copy a to output initially
        qc.cx(qr_input_a[2-i], qr_output[2-i])
        
        # Compute AND between a and b, store temporarily in b register
        qc.ccx(qr_input_a[2-i], qr_input_b[2-i], qr_input_b[2-i])  # This modifies b register temporarily
        
        # Now XOR the result of AND with both a and b
        qc.cx(qr_input_b[2-i], qr_output[2-i])
        
        # Restore original b value by applying X gate if original bit was 1
        # Actually, we need to reset the temporary storage
        # Let's take a different approach: directly implement OR using ancillas
        
    # Reset circuit and implement correctly
    qc = QuantumCircuit(qr_input_a, qr_input_b, qr_output, cr_output)
    
    # Reinitialize inputs
    for i in range(3):
        if a_bits[i] == '1':
            qc.x(qr_input_a[2-i])
        if b_bits[i] == '1':
            qc.x(qr_input_b[2-i])
    
    # Implement OR gate for each bit position
    for i in range(3):
        pos = 2-i  # Position in quantum register (reverse order)
        # OR gate implementation: 
        # We'll use an ancilla qubit to help compute OR from AND
        # OR(a,b) = NOT(AND(NOT(a), NOT(b)))
        
        # Since we don't have extra ancillas, implement directly
        # OR(a,b) means result is 1 if a=1 or b=1 or both
        # We can use: result = a XOR b XOR (a AND b)
        
        # First copy 'a' to output
        qc.cx(qr_input_a[pos], qr_output[pos])
        
        # Then XOR 'b' to output (this gives A XOR B)
        qc.cx(qr_input_b[pos], qr_output[pos])
        
        # Then XOR (A AND B) to output to get final OR
        # Use input_b[pos] as temporary storage for A AND B
        qc.ccx(qr_input_a[pos], qr_input_b[pos], qr_output[pos])
    
    # Measure the output
    qc.measure(qr_output, cr_output)
    
    # Simulate the circuit
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1024).result()
    counts = result.get_counts(qc)
    
    # Return probability distribution
    total_shots = sum(counts.values())
    prob_dist = {key: count/total_shots for key, count in counts.items()}
    
    return prob_dist
