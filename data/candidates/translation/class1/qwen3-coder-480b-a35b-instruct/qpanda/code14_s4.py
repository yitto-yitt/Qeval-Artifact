# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import *
from pyqpanda3.machine import *

def bell_each_shot():
    # Initialize quantum machine
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Create quantum program
    prog = QProg()
    
    # Allocate qubits and classical bits
    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)
    
    # Build Bell circuit
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
    prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    
    # Run the program for 10 shots
    result = qvm.run_with_configuration(prog, c, 10)
    
    # Process results to get counts
    counts = {}
    for res in result:
        bitstring = ''.join(str(res[i]) for i in range(len(c)))
        if bitstring in counts:
            counts[bitstring] += 1
        else:
            counts[bitstring] = 1
    
    # Convert counts to probabilities
    total = sum(counts.values())
    prob_dist = {key: value / total for key, value in counts.items()}
    
    # Release resources
    qvm.finalize()
    
    return prob_dist
