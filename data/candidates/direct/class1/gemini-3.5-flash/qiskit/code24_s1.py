# EVAL_META: task_id=24, framework=qiskit, class=1

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    N = oracle.num_qubits
    n = N - 1
    
    dj_circuit = QuantumCircuit(N, n)
    
    # Put output qubit in state |->
    dj_circuit.x(n)
    dj_circuit.h(n)
    
    # Put input qubits in state |+>
    for i in range(n):
        dj_circuit.h(i)
        
    # Apply oracle
    if isinstance(oracle, QuantumCircuit):
        dj_circuit.compose(oracle, inplace=True)
    else:
        dj_circuit.append(oracle, range(N))
        
    # Apply H-gates to input qubits
    for i in range(n):
        dj_circuit.h(i)
        
    # Measure input qubits
    dj_circuit.measure(range(n), range(n))
    
    # Run simulation
    simulator = AerSimulator()
    compiled_circuit = transpile(dj_circuit, simulator)
    result = simulator.run(compiled_circuit, shots=1024).result()
    counts = result.get_counts()
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    probabilities = {bitstr: count / total_shots for bitstr, count in counts.items()}
    
    return probabilities
