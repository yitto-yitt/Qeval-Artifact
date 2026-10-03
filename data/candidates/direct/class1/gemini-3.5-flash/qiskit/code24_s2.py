# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle: QuantumCircuit) -> dict:
    num_qubits = oracle.num_qubits
    n = num_qubits - 1
    
    # Create the Deutsch-Jozsa circuit
    qc = QuantumCircuit(num_qubits, n)
    
    # Initialize the output qubit to |1>
    qc.x(n)
    
    # Apply Hadamard gates to all qubits
    qc.h(range(num_qubits))
    
    # Apply the oracle
    qc.compose(oracle, inplace=True)
    
    # Apply Hadamard gates to the input qubits
    qc.h(range(n))
    
    # Measure the input qubits
    qc.measure(range(n), range(n))
    
    # Execute the circuit using AerSimulator
    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate the probability distribution
    total_shots = sum(counts.values())
    probability_distribution = {bitstr: count / total_shots for bitstr, count in counts.items()}
    
    return probability_distribution
