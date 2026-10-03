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
    q = machine.qAlloc_many(n_qubits)
    c = machine.cAlloc_many(n_qubits - 1)
    
    prog = QProg()
    
    # Apply X gate to the last qubit
    prog << X(q[n_qubits - 1])
    
    # Apply H gates to all qubits
    for i in range(n_qubits):
        prog << H(q[i])
    
    # Apply the oracle (this needs to be implemented as a quantum circuit)
    # Since oracle is typically a unitary matrix, we need to decompose it or apply it differently
    # For now, assuming oracle is provided as a QProg or can be converted to one
    if hasattr(oracle, '__call__'):
        # If oracle is a function that builds a circuit
        oracle_circuit = oracle(q)
        prog << oracle_circuit
    else:
        # If oracle is already a QProg or similar construct
        prog << oracle
    
    # Apply H gates again to all qubits except the last one
    for i in range(n_qubits - 1):
        prog << H(q[i])
    
    # Measure all input qubits (all except the last one)
    for i in range(n_qubits - 1):
        prog << Measure(q[i], c[i])
    
    # Run the program
    result = run_with_configuration(machine, prog, c, 1024)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    destroy_quantum_machine(machine)
    return prob_dist
