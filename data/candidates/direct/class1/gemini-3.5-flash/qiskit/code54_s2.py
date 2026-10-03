# EVAL_META: task_id=54, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def and_gate(a: int, b: int) -> dict:
    qc = QuantumCircuit(9, 3)
    
    # Initialize register a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
            
    # Initialize register b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
            
    # Apply bitwise AND using Toffoli gates
    for i in range(3):
        qc.ccx(i, 3 + i, 6 + i)
        
    # Measure the result register
    for i in range(3):
        qc.measure(6 + i, i)
        
    # Simulate the circuit
    simulator = AerSimulator()
    qc_transpiled = transpile(qc, simulator)
    result = simulator.run(qc_transpiled, shots=1024).result()
    counts = result.get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
