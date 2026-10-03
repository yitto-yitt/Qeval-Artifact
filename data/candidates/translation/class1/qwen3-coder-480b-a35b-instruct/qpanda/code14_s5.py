# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import QProg, Qubit, CBit
from pyqpanda3.algorithms import *
from pyqpanda3 import *

def bell_each_shot():
    # Initialize quantum machine
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    
    # Create quantum program
    prog = QProg()
    
    # Allocate qubits and classical bits
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    
    # Build Bell circuit (phi+ state)
    prog << pq.H(qubits[0])
    prog << pq.CNOT(qubits[0], qubits[1])
    prog << pq.Measure(qubits[0], cbits[0])
    prog << pq.Measure(qubits[1], cbits[1])
    
    # Run the program for 10 shots
    result = qvm.run_with_configuration(prog, cbits, 10)
    
    # Process results to get counts
    counts = {}
    for res in result:
        bitstring = ''.join([str(res[i]) for i in range(len(cbits)-1, -1, -1)])
        if bitstring in counts:
            counts[bitstring] += 1
        else:
            counts[bitstring] = 1
    
    # Calculate probabilities
    total_shots = sum(counts.values())
    prob_dist = {key: value / total_shots for key, value in counts.items()}
    
    # Release resources
    qvm.destroy_qvm()
    
    return prob_dist
