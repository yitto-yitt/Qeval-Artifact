# EVAL_META: task_id=24, framework=qiskit, class=1
from qiskit import QuantumCircuit
from qiskit_aer import Aer

def dj_algorithm(oracle):
    """
    Given a Deutsch-Jozsa oracle (a QuantumCircuit) where the final qubit is the output qubit,
    runs the Deutsch-Jozsa routine and returns a probability distribution dict for the measured
    input-register bitstrings.
    """
    n = oracle.num_qubits - 1
    # Create a circuit with n+1 qubits and n classical bits for the input register
    qc = QuantumCircuit(n + 1, n)
    
    # Initialize the output qubit to |1>
    qc.x(n)
    
    # Apply Hadamard to all qubits
    qc.h(range(n + 1))
    
    # Apply the oracle
    qc.append(oracle.to_instruction(), range(n + 1))
    
    # Apply Hadamard to the input register
    qc.h(range(n))
    
    # Measure the input register
    qc.measure(range(n), range(n))
    
    # Run the circuit on the QASM simulator
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(qc, shots=1024)
    counts = job.result().get_counts()
    
    # Convert counts to probabilities
    prob_dict = {key: value / 1024.0 for key, value in counts.items()}
    
    return prob_dict
