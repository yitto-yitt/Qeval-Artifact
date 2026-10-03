# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit_aer import AerSimulator
from qiskit import transpile


def or_gate(a, b):
    # Create quantum registers for input a, input b, and output
    qreg = QuantumRegister(9, 'q')  # 3 qubits for a, 3 for b, 3 for output
    creg = ClassicalRegister(3, 'c')  # 3 classical bits for measurement
    circuit = QuantumCircuit(qreg, creg)
    
    # Encode integer a into first 3 qubits (q[0], q[1], q[2])
    for i in range(3):
        if (a >> i) & 1:
            circuit.x(qreg[i])
    
    # Encode integer b into next 3 qubits (q[3], q[4], q[5])
    for i in range(3):
        if (b >> i) & 1:
            circuit.x(qreg[3 + i])
    
    # Implement bitwise OR using ancilla qubits for each bit position
    # For each bit position i, we compute a[i] OR b[i] and store in q[6+i]
    for i in range(3):
        # Use the identity: x OR y = NOT(NOT(x) AND NOT(y))
        # First, copy a[i] and b[i] to ancilla qubits
        circuit.cx(qreg[i], qreg[6 + i])  # Copy a[i] to output
        # If b[i] is 1, set output to 1 (OR behavior)
        circuit.x(qreg[3 + i])  # Flip b[i] 
        circuit.ccx(qreg[3 + i], qreg[i], qreg[6 + i])  # If both were 1, keep output as 1
        circuit.x(qreg[3 + i])  # Flip back b[i]
        
        # Alternative simpler approach using X gates and Toffoli:
        # To implement OR: if either input is 1, output should be 1
        # We can do: output = a OR b = NOT((NOT a) AND (NOT b))
        # But simpler direct approach:
        # Just set output to 1 if either a or b is 1
        # This can be done with controlled operations
    
    # Simpler correct implementation of OR gate:
    # For each bit position, we want output = a OR b
    # We'll use a different approach:
    circuit.reset(qreg[6])  
    circuit.reset(qreg[7])  
    circuit.reset(qreg[8])  
    
    # Reimplement correctly:
    # To compute OR: we start with |a>|b>|0> and want |a>|b>|a OR b>
    for i in range(3):
        # Initialize output qubit to 0 - it already is
        
        # Apply OR logic: if a[i]=1 or b[i]=1, then output[i]=1
        # This can be achieved by:
        # 1. Copy a[i] to output[i] 
        circuit.cx(qreg[i], qreg[6 + i])
        # 2. If b[i]=1, set output[i]=1 regardless of current value
        circuit.x(qreg[3 + i])  # temporarily flip b[i]
        circuit.cx(qreg[3 + i], qreg[6 + i])  # if b[i] was 1, flip output[i]
        circuit.x(qreg[3 + i])  # flip back b[i]
    
    # Measure the output qubits
    for i in range(3):
        circuit.measure(qreg[6 + i], creg[i])
    
    # Run on simulator
    simulator = AerSimulator()
    compiled_circuit = transpile(circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    # Normalize to get probability distribution
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    return prob_dist
