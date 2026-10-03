# EVAL_META: task_id=53, framework=cirq, class=1
import cirq
import collections

def xor_gate(a, b):
    # Create qubits
    qubits = cirq.LineQubit.range(8)
    
    # Convert integers to binary strings (padded to 8 bits)
    a_bits = format(a, '08b')
    b_bits = format(b, '08b')
    
    # Build the circuit
    circuit = cirq.Circuit()
    
    # Apply X gates for the first input
    for i in range(8):
        if a_bits[i] == '1':
            circuit.append(cirq.X(qubits[i]))
    
    # Apply CNOT gates for XOR with second input
    for i in range(8):
        if b_bits[i] == '1':
            circuit.append(cirq.CNOT(cirq.LineQubit(8), qubits[i]))  # Use ancilla for control
    
    # Actually, let's do this properly - XOR is just addition mod 2
    # We'll use a simpler approach: XOR(a,b) = (a AND NOT b) OR (NOT a AND b)
    # But even simpler: we can just compute a^b classically and encode it
    # However, following the quantum spirit, let's do it with CNOTs properly
    
    # Recreate properly: 
    # To simulate XOR(a,b), we can initialize qubits to 'a' and then XOR with 'b'
    # XOR between two bitstrings is done by applying CNOT for each bit position where b has 1
    
    circuit = cirq.Circuit()
    
    # Initialize qubits to represent 'a'
    for i in range(8):
        if a_bits[i] == '1':
            circuit.append(cirq.X(qubits[i]))
    
    # Apply XOR with b - CNOT controls on b's bits, targets on our qubits
    # But we need to make b classical controls into quantum - so we'd need ancillas
    # Simpler approach: directly apply the XOR result since we know it classically
    
    # Let's follow what the Qiskit XOR does more closely:
    # XOR(n, value) creates a circuit that encodes value into n qubits
    # So XOR(8,a).compose(XOR(8,b)) means: encode a, then XOR with b
    # In Cirq terms: start with |0>, apply XOR with a, then XOR with b
    # XOR with a known value is just flipping qubits where that value has 1s
    
    # Actually re-reading: XOR(8,a) encodes a into 8 qubits
    # Then XOR(8,b) would XOR b onto those same qubits
    # This is equivalent to just encoding (a XOR b) directly
    
    # But to maintain the structure, let's build it step by step:
    circuit = cirq.Circuit()
    
    # First, encode 'a' 
    for i in range(8):
        if a_bits[i] == '1':
            circuit.append(cirq.X(qubits[i]))
            
    # Then XOR with 'b' - which means flip qubit i if b_bits[i] is 1
    for i in range(8):
        if b_bits[i] == '1':
            circuit.append(cirq.X(qubits[i]))
    
    # Add measurements
    circuit.append(cirq.measure(*qubits, key='result'))
    
    # Run simulation
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=10000)
    
    # Get measurement results
    measurements = result.data['result']
    
    # Convert to bitstrings and count
    counts = collections.Counter()
    for _, row in measurements.iterrows():
        # Row contains integers; convert to bitstring
        bitstring = format(row[0], '08b')
        counts[bitstring] += 1
        
    # Normalize to probabilities
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
