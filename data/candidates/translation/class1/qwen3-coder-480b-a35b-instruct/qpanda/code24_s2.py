# EVAL_META: task_id=24, framework=qpanda, class=1
import pyqpanda3 as pq
from pyqpanda3.core import *
from pyqpanda3 import *

def dj_algorithm(oracle):
    n = oracle.get_qubit_number()
    machine = pq.QMachine()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n - 1)
    
    prog = pq.QProg()
    
    # Apply X gate to the last qubit
    prog << X(qubits[n - 1])
    
    # Apply H gates to all qubits
    for i in range(n):
        prog << H(qubits[i])
    
    # Add the oracle
    prog << oracle
    
    # Apply H gates again to all qubits
    for i in range(n):
        prog << H(qubits[i])
    
    # Measure the first n-1 qubits
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
    
    result = machine.run(prog)
    
    # Get the count results
    counts = result
    total = sum(counts.values())
    
    # Normalize the counts to get probabilities
    prob_dist = {}
    for key, value in counts.items():
        prob_dist[key] = value / total
    
    machine.finalize()
    return prob_dist
