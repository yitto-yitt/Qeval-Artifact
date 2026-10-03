# EVAL_META: task_id=56, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

def not_gate(a):
    """Return probability distribution of bitwise NOT of 8-bit integer a."""
    # Create a circuit with 8 qubits and 8 classical bits
    qc = QuantumCircuit(8, 8)
    
    # Set initial state to bit representation of a (qubit i <- bit i of a, LSB)
    for i in range(8):
        if (a >> i) & 1:
            qc.x(i)
    
    # Apply bitwise NOT (X on all qubits)
    for i in range(8):
        qc.x(i)
    
    # Measure all qubits
    qc.measure(range(8), range(8))
    
    # Simulate with 1024 shots
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Normalize to probabilities
    total_shots = 1024
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    return prob_dist
