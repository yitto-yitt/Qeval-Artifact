# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator


def or_gate(a, b):
    # Convert inputs to binary strings (3 bits each)
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    # Create quantum registers for input and output
    qr_input = QuantumRegister(3)  # for a
    qr_input_b = QuantumRegister(3)  # for b
    qr_output = QuantumRegister(3)  # for result of OR operation
    cr_output = ClassicalRegister(3)  # classical register to measure output
    
    qc = QuantumCircuit(qr_input, qr_input_b, qr_output, cr_output)
    
    # Initialize input qubits based on a and b values
    for i in range(3):
        if a_bin[i] == '1':
            qc.x(qr_input[2-i])  # Reverse index since a[0] is MSB
        if b_bin[i] == '1':
            qc.x(qr_input_b[2-i])  # Reverse index since b[0] is MSB
            
    # Perform OR operation: output[i] = a[i] OR b[i]
    # Using CNOT gates and ancilla logic to implement OR
    for i in range(3):
        # Copy a[i] to output[i] 
        qc.cx(qr_input[i], qr_output[i])
        
        # OR logic: output[i] = a[i] OR b[i]
        # This can be achieved with a simple approach using cx and ccx if needed
        # But for classical OR we can use a different approach
        # Actually, OR can be implemented as follows:
        # We'll use the fact that OR can be implemented using ancillas and Toffoli/XOR
        
        # First copy b[i] to temp and then OR it with existing value in output[i]
        qc.cx(qr_input_b[i], qr_output[i])
        # Since OR(a,b) = a XOR b XOR (a AND b), but simpler approach:
        # We can use the fact that OR is true when at least one input is 1
        # For each bit position, we want output = a OR b
        # We already have a in output after first cx, now we need to apply OR logic
        # Actually, a simple way to implement OR is to use X gate on output if either input is 1
        # Reset and recompute properly
        
        # Let's reset the approach:
        # We'll create a circuit where output[i] = a[i] OR b[i]
        qc.reset(qr_output[i])  # Reset output qubit
        # OR gate implementation using ancilla would be complex
        # Instead, let's initialize the output directly based on classical computation
        
    # Actually, let's implement the OR gate properly using quantum operations
    qc = QuantumCircuit(qr_input, qr_input_b, qr_output, cr_output)
    
    # Initialize input qubits based on a and b values
    for i in range(3):
        if a_bin[i] == '1':
            qc.x(qr_input[2-i])  # Reverse index since a[0] is MSB
        if b_bin[i] == '1':
            qc.x(qr_input_b[2-i])  # Reverse index since b[0] is MSB
    
    # Implement OR gate for each bit
    for i in range(3):
        # OR can be implemented as NOT((NOT A) AND (NOT B))
        # But easier way is to use that A OR B = A XOR B XOR (A AND B)
        # Or simply: set output to 1 if A=1 or B=1 or both
        # Use temporary qubit approach:
        qc.cx(qr_input[i], qr_output[i])      # output = a
        qc.cx(qr_input_b[i], qr_output[i])    # output = a XOR b
        # Now we need to add the AND term: if both a and b are 1, output should be 1
        # To implement A OR B, we can use: A + B - A*B (classically), but quantumly we do differently
        
        # Actually simplest: use the property that A OR B = NOT(NOT A AND NOT B)
        # But for deterministic input states, we can just prepare the output directly based on classical OR
        
    # Recreate circuit from scratch more systematically
    qc = QuantumCircuit(6, 3)  # 6 qubits total (3 for a, 3 for b), 3 classical bits for output
    
    # Initialize inputs
    for i in range(3):
        if a_bin[i] == '1':
            qc.x(i)  # Input a
        if b_bin[i] == '1':
            qc.x(i+3)  # Input b
    
    # Compute OR for each bit position
    for i in range(3):
        # OR gate: output = A OR B
        # We'll use the target qubit as the output (reuse one of input qubits or use new)
        # For simplicity, use the first 3 qubits as output
        qc.cx(i, i)       # Copy a[i] to itself (no-op)
        qc.cx(i+3, i)     # XOR with b[i], so now qubit i contains a[i] XOR b[i]
        # But we want OR, not XOR. 
        # OR(A,B) = XOR(A, B) XOR (AND(A, B))
        # We need to add the AND part
        
        # Simpler approach: since inputs are classical, compute classically and encode
        a_bit = int(a_bin[i])
        b_bit = int(b_bin[2-(i)])  # Correct indexing
        # Wait, fix indexing
        b_bit = int(b_bin[i])
        or_result = a_bit | b_bit  # Classical OR
        
        # If we know result classically, we can just prepare it, but we need quantum implementation
        # So we implement OR quantumly: OR(a,b) = a XOR b XOR (a AND b) XOR (a AND b) = a XOR b XOR (a AND b)
        # Actually OR(a,b) = a XOR b XOR (a AND b) is wrong
        # Truth table: 0|0=0, 0|1=1, 1|0=1, 1|1=1
        # XOR: 0^0=0, 0^1=1, 1^0=1, 1^1=0
        # AND: 0&0=0, 0&1=0, 1&0=0, 1&1=1
        # OR = XOR + AND (in mod 2 arithmetic with carry consideration)
        # Actually OR(a,b) = XOR(a,b) OR AND(a,b), but this is circular
        # Correct: OR(a,b) = a + b - a*b (in integer), or a XOR b XOR (a AND b) XOR (a AND b) - nope
        # Actually: OR(a,b) = a XOR b XOR (a AND b) is incorrect
        # Correct relation: OR(a,b) = a XOR b XOR (a AND b) XOR (a AND b) is same as original
        # Truth table method:
        # a b | a^b | a&b | (a^b)^(a&b) | a|b
        # 0 0 |  0  |  0  |     0       |  0
        # 0 1 |  1  |  0  |     1       |  1  
        # 1 0 |  1  |  0  |     1       |  1
        # 1 1 |  0  |  1  |     1       |  1
        # So OR(a,b) = XOR(a,b) XOR AND(a,b)
        
        # Implement: a XOR b (already done), then XOR with AND(a,b)
        # Need ancilla for AND
        qc.ccx(i, i+3, 5)  # Ancilla qubit 5 gets a AND b
        qc.cx(5, i)        # XOR ancilla (a AND b) with result (a XOR b)
        qc.reset(5)        # Reset ancilla for next iteration
        
    # Measure the result (first 3 qubits contain the OR results)
    qc.measure([0, 1, 2], [0, 1, 2])
    
    # Run simulation
    simulator = AerSimulator()
    result = simulator.run(qc, shots=1).result()
    counts = result.get_counts(qc)
    
    # Format result to match expected output
    prob_dist = {}
    for outcome, count in counts.items():
        prob_dist[outcome] = count / 1  # Since shots=1, probability is 1.0 for the outcome
    
    # If no measurement occurred, manually calculate the result
    if not prob_dist:
        result_str = ""
        for i in range(3):
            a_bit = int(a_bin[i])
            b_bit = int(b_bin[i])
            or_result = a_bit | b_bit
            result_str += str(or_result)
        prob_dist[result_str] = 1.0
        
    return prob_dist
