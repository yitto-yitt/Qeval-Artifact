# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def not_gate(a: int) -> dict:
    # Ensure a is within 8-bit range
    a = a & 0xFF
    
    # Create a quantum circuit with 8 qubits and 8 classical bits
    qc = QuantumCircuit(8, 8)
    
    # Convert 'a' to an 8-bit binary string (MSB to LSB)
    a_bin = f"{a:08b}"
    
    # Initialize the qubits to the state representing 'a'
    # Qiskit qubit 0 corresponds to the LSB (rightmost bit)
    for i in range(8):
        bit = int(a_bin[7 - i])
        if bit == 1:
            qc.x(i)
            
    # Apply bitwise NOT gate (X gate) to all qubits
    for i in range(8):
        qc.x(i)
        
    # Measure all qubits
    qc.measure(range(8), range(8))
    
    # Simulate the circuit
    simulator = AerSimulator()
    qc_transpiled = transpile(qc, simulator)
    result = simulator.run(qc_transpiled, shots=1024).result()
    counts = result.get_counts()
    
    # Convert counts to probability distribution
    total_shots = sum(counts.values())
    prob_dist = {state: count / total_shots for state, count in counts.items()}
    
    return prob_dist
