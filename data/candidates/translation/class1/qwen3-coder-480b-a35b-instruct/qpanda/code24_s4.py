# EVAL_META: task_id=24, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3 import *

def dj_algorithm(oracle):
    # Get the number of qubits from the oracle
    n = oracle.get_qubit_num()
    
    # Create quantum and classical registers
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n - 1)
    
    # Build the circuit
    prog = pq.QProg()
    
    # Initialize the last qubit to |1>
    prog << X(qubits[n - 1])
    
    # Apply Hadamard to all qubits
    for i in range(n):
        prog << H(qubits[i])
    
    # Apply the oracle (assuming it's provided as a QProg or similar structure)
    prog << oracle
    
    # Apply Hadamard to all qubits again
    for i in range(n):
        prog << H(qubits[i])
    
    # Measure the first n-1 qubits
    for i in range(n - 1):
        prog << pq.Measure(qubits[i], cbits[i])
    
    # Run the program
    result = machine.run(prog)
    
    # Extract counts
    counts = {}
    for key, value in result.items():
        counts[key] = value
    
    # Calculate probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    # Clean up
    machine.finalize()
    
    return prob_dist
