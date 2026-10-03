# EVAL_META: task_id=15, framework=qpanda, class=1
import pyqpanda3.core as pq
from pyqpanda3.core import *
import numpy as np

def noisy_bell():
    # Create quantum program
    qvm = pq.QVM()
    qvm.init_qvm()
    
    # Allocate qubits and classical bits
    qubits = qvm.qAlloc_many(2)
    cbit = qvm.cAlloc_many(2)
    
    # Build Bell circuit
    prog = pq.QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
    prog << MEASURE(qubits[0], cbit[0]) << MEASURE(qubits[1], cbit[1])
    
    # Run the program
    result = qvm.run_with_configuration(prog, cbit, 1000)
    
    # Process results to get probability distribution
    counts = {}
    for outcome, count in result.items():
        # Reverse the bitstring to match Qiskit's convention (qubit order)
        reversed_outcome = outcome[::-1]
        counts[reversed_outcome] = count
    
    total = sum(counts.values())
    probabilities = {key: value / total for key, value in counts.items()}
    
    qvm.finalize()
    
    return probabilities
