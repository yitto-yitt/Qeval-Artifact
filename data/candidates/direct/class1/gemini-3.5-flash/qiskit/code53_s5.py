# EVAL_META: task_id=53, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def xor_gate(a: int, b: int) -> dict:
    # Create a quantum circuit with 8 qubits and 8 classical bits
    qc = QuantumCircuit(8, 8)
    
    for i in range(8):
        # Extract the i-th bit (LSB is index 0)
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        
        if bit_a:
            qc.x(i)
        if bit_b:
            qc.x(i)
            
    qc.measure(range(8), range(8))
    
    # Run the simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Normalize counts to probabilities
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
