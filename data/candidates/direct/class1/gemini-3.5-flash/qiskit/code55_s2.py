# EVAL_META: task_id=55, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def or_gate(a: int, b: int) -> dict:
    """
    Given two 3-bit integers a and b, design a quantum circuit that acts as a 
    bitwise classical OR gate and sample the output.
    Returns a probability distribution dict keyed by 3-bit measurement strings.
    """
    qc = QuantumCircuit(9, 3)
    
    # Initialize input states
    for i in range(3):
        val_a = (a >> i) & 1
        val_b = (b >> i) & 1
        if val_a:
            qc.x(i)
        if val_b:
            qc.x(i + 3)
            
    # Compute bitwise OR using cx and ccx gates
    # c_i = a_i ^ b_i ^ (a_i & b_i)
    for i in range(3):
        qc.cx(i, i + 6)
        qc.cx(i + 3, i + 6)
        qc.ccx(i, i + 3, i + 6)
        
    # Measure the result qubits
    for i in range(3):
        qc.measure(i + 6, i)
        
    # Run the simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Convert counts to probabilities
    total_shots = sum(counts.values())
    probabilities = {state: count / total_shots for state, count in counts.items()}
    
    return probabilities
