# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def not_gate(a: int) -> dict:
    # Represent the 8-bit integer as a binary string
    binary_str = f"{a:08b}"
    
    qc = QuantumCircuit(8, 8)
    
    # Initialize the qubits to represent the integer a
    # Qiskit LSB is at index 0, so we map binary_str[7-i] to qubit i
    for i in range(8):
        if binary_str[7 - i] == '1':
            qc.x(i)
            
    # Apply NOT gate (X gate) to all qubits
    for i in range(8):
        qc.x(i)
        
    # Measure all qubits
    qc.measure(range(8), range(8))
    
    # Run the simulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate probability distribution
    total_shots = sum(counts.values())
    prob_dist = {state: count / total_shots for state, count in counts.items()}
    
    return prob_dist
