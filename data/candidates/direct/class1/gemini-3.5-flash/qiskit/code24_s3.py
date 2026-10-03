# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle: QuantumCircuit) -> dict:
    num_qubits = oracle.num_qubits
    n_inputs = num_qubits - 1
    
    qc = QuantumCircuit(num_qubits, n_inputs)
    
    # Initialize input qubits in |+>
    for q in range(n_inputs):
        qc.h(q)
        
    # Initialize output qubit in |->
    qc.x(n_inputs)
    qc.h(n_inputs)
    
    # Apply oracle
    qc.compose(oracle, inplace=True)
    
    # Apply H to input qubits
    for q in range(n_inputs):
        qc.h(q)
        
    # Measure input qubits
    qc.measure(range(n_inputs), range(n_inputs))
    
    # Run simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
