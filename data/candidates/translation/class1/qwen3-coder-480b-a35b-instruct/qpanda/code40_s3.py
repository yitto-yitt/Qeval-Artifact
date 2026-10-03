# EVAL_META: task_id=40, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def init_random_3qubit(desired_vector):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(3)
    cbits = machine.cAlloc_many(3)
    
    prog = pq.QProg()
    
    # Create the desired state initialization using U3 gates
    # We need to decompose the desired_vector into appropriate rotations
    state = desired_vector
    
    # Apply state preparation using amplitude encoding approach
    # For 8-dimensional state vector, we need to find appropriate rotation angles
    qcircuit = pq.QCircuit()
    
    # Direct state preparation using U gates based on the desired vector
    # First, create the circuit that prepares the state
    psi = np.array(state)
    psi_normalized = psi / np.linalg.norm(psi)
    
    # Build the circuit using pyQPanda's state preparation method
    prog.insert(pq.initState(qubits, psi_normalized))
    
    # Measure all qubits
    for i in range(3):
        prog.insert(pq.Measure(qubits[i], cbits[i]))
    
    result = machine.run(prog)
    
    # Count the results
    counts = {}
    for res in result:
        bits = ''.join(['1' if b else '0' for b in res])
        counts[bits] = counts.get(bits, 0) + 1
    
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    machine.finalize()
    
    return prob_dist
