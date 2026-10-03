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
    
    # Apply the oracle
    prog << oracle
    
    # Apply Hadamard to all qubits again
    for i in range(n):
        prog << H(qubits[i])
    
    # Measure the first n-1 qubits
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
    
    # Run the program
    result = machine.run(prog)
    
    # Get the measurement results
    counts = {}
    for res in result:
        bitstring = ""
        for i in range(n - 1):
            bitstring += str(res[cbits[i]])
        if bitstring in counts:
            counts[bitstring] += 1
        else:
            counts[bitstring] = 1
    
    # Calculate probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    # Free allocated resources
    machine.qFree_all()
    machine.cFree_all()
    
    return prob_dist
