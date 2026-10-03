# EVAL_META: task_id=55, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a: int, b: int) -> dict:
    # Create a quantum circuit with 9 qubits and 3 classical bits
    # Qubits 0-2: a
    # Qubits 3-5: b
    # Qubits 6-8: c (result)
    qc = QuantumCircuit(9, 3)
    
    # Initialize qubits for a
    for i in range(3):
        if (a >> i) & 1:
            qc.x(i)
            
    # Initialize qubits for b
    for i in range(3):
        if (b >> i) & 1:
            qc.x(3 + i)
            
    # Compute bitwise OR: c_i = a_i OR b_i
    # Using the identity: a OR b = a ^ b ^ (a & b)
    for i in range(3):
        qc.cx(i, 6 + i)
        qc.cx(3 + i, 6 + i)
        qc.ccx(i, 3 + i, 6 + i)
        
    # Measure the result qubits 6-8 into classical bits 0-2
    for i in range(3):
        qc.measure(6 + i, i)
        
    # Run the simulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Normalize counts to probabilities
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
