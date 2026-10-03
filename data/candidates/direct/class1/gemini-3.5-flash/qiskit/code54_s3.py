# EVAL_META: task_id=54, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def and_gate(a: int, b: int) -> dict:
    # We need 3 qubits for a, 3 for b, 3 for the result, and 3 classical bits
    qc = QuantumCircuit(9, 3)
    
    # Initialize register A (qubits 0, 1, 2) and B (qubits 3, 4, 5)
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
        if (b >> i) & 1:
            qc.x(i + 3)
            
    # Perform bitwise AND using CCNOT (Toffoli) gates
    for i in range(3):
        qc.ccx(i, i + 3, i + 6)
        
    # Measure the result register (qubits 6, 7, 8) into classical bits 0, 1, 2
    for i in range(3):
        qc.measure(i + 6, i)
        
    # Simulate the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(compiled_circuit)
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
