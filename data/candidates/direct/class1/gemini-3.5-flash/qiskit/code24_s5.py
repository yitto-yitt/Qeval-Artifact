# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle: QuantumCircuit) -> dict:
    n = oracle.num_qubits
    # n-1 input qubits, 1 output qubit
    dj_circuit = QuantumCircuit(n, n - 1)
    
    # State preparation: output qubit to |1>
    dj_circuit.x(n - 1)
    
    # Apply H to all qubits
    for i in range(n):
        dj_circuit.h(i)
        
    # Apply oracle
    dj_circuit.compose(oracle, range(n), inplace=True)
    
    # Apply H to input qubits
    for i in range(n - 1):
        dj_circuit.h(i)
        
    # Measure input qubits
    dj_circuit.measure(range(n - 1), range(n - 1))
    
    # Run simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(dj_circuit, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
