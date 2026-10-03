# EVAL_META: task_id=55, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a: int, b: int) -> dict:
    # Create a quantum circuit with 9 qubits and 3 classical bits
    # Qubits 0-2: input a
    # Qubits 3-5: input b
    # Qubits 6-8: output c = a OR b
    qc = QuantumCircuit(9, 3)
    
    # Initialize input a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
            
    # Initialize input b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
            
    # Compute bitwise OR using De Morgan's Law: a OR b = NOT( NOT(a) AND NOT(b) )
    for i in range(3):
        qc.x(i)
        qc.x(3 + i)
        qc.ccx(i, 3 + i, 6 + i)
        qc.x(6 + i)
        
    # Measure the output qubits (6, 7, 8) into classical bits (0, 1, 2)
    qc.measure([6, 7, 8], [0, 1, 2])
    
    # Run the simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Convert counts to a probability distribution
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
