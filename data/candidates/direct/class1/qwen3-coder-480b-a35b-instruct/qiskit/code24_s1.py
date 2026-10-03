# EVAL_META: task_id=24, framework=qiskit, class=1

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator

def dj_algorithm(oracle):
    # Get the number of qubits from the oracle
    n = oracle.num_qubits - 1  # Exclude the output qubit
    
    # Create quantum and classical registers
    qr = QuantumRegister(n + 1, 'q')
    cr = ClassicalRegister(n, 'c')
    
    # Create the circuit
    dj_circuit = QuantumCircuit(qr, cr)
    
    # Apply H-gates to all qubits except the last one (output qubit)
    for i in range(n):
        dj_circuit.h(i)
    
    # Prepare the output qubit in the |−⟩ state
    dj_circuit.x(n)  # X gate to make it |1⟩
    dj_circuit.h(n)  # Hadamard to create |−⟩ state
    
    # Add the oracle
    dj_circuit.compose(oracle, inplace=True)
    
    # Apply H-gates to the input register again
    for i in range(n):
        dj_circuit.h(i)
    
    # Measure the input register
    for i in range(n):
        dj_circuit.measure(i, i)
    
    # Run the circuit on a simulator
    backend = AerSimulator()
    job = backend.run(dj_circuit, shots=1000)
    result = job.result()
    
    # Get the counts and convert to probabilities
    counts = result.get_counts(dj_circuit)
    total_shots = sum(counts.values())
    probabilities = {key: value / total_shots for key, value in counts.items()}
    
    return probabilities
