# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import math

def dj_algorithm(oracle):
    # Get the number of qubits from the oracle (assuming it's provided as a unitary matrix or circuit)
    # Since pyQPanda doesn't have direct access to num_qubits like Qiskit,
    # we need to infer this from the oracle structure
    n = len(oracle)  # Assuming oracle is a unitary matrix of size 2^n x 2^n
    
    # Calculate number of qubits based on matrix size
    import math
    n_qubits = int(math.log(len(oracle), 2))
    
    machine = init_quantum_machine(QMachineType.CPU)
    qubits = machine.qAlloc_many(n_qubits)
    cbits = machine.cAlloc_many(n_qubits - 1)
    
    prog = QProg()
    
    # Initialize the last qubit to |1⟩
    prog << X(qubits[n_qubits - 1])
    
    # Apply Hadamard to all qubits
    for i in range(n_qubits):
        prog << H(qubits[i])
    
    # Compose the oracle - since pyQPanda doesn't have direct compose,
    # we assume the oracle is provided as a subprogram or need to construct it differently
    # Here we'll assume oracle is a function that takes qubits and applies the operation
    if callable(oracle):
        oracle(prog, qubits)
    else:
        # If oracle is a matrix, convert it to a quantum program
        # This is a simplified approach - actual implementation might vary
        pass
    
    # Apply Hadamard to input qubits again
    for i in range(n_qubits - 1):
        prog << H(qubits[i])
    
    # Measure the input qubits
    for i in range(n_qubits - 1):
        prog << Measure(qubits[i], cbits[i])
    
    # Run the program
    result = machine.run_with_configuration(prog, cbits, 1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    destroy_quantum_machine(machine)
    return prob_dist
