# EVAL_META: task_id=24, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    n_qubits = oracle.num_qubits
    n_inputs = n_qubits - 1
    
    dj_circuit = QuantumCircuit(n_qubits, n_inputs)
    
    # Initialize the output qubit to |1>
    dj_circuit.x(n_inputs)
    
    # Apply Hadamard gates to all qubits
    for i in range(n_qubits):
        dj_circuit.h(i)
        
    # Apply the oracle
    if isinstance(oracle, QuantumCircuit):
        dj_circuit.compose(oracle, range(n_qubits), inplace=True)
    else:
        dj_circuit.append(oracle, range(n_qubits))
        
    # Apply Hadamard gates to the input qubits
    for i in range(n_inputs):
        dj_circuit.h(i)
        
    # Measure the input qubits
    dj_circuit.measure(range(n_inputs), range(n_inputs))
    
    # Execute the circuit
    simulator = AerSimulator()
    compiled_circuit = transpile(dj_circuit, simulator)
    result = simulator.run(compiled_circuit, shots=1024).result()
    counts = result.get_counts()
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    probabilities = {bitstring: count / total_shots for bitstring, count in counts.items()}
    
    return probabilities
