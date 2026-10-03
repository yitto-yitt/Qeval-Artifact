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
    cbits = qvm.cAlloc_many(2)
    
    # Build Bell circuit
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    prog.insert(pq.Measure(qubits[1], cbits[1]))
    
    # Run the program multiple times to simulate shots
    shots = 1000
    results = {}
    
    for _ in range(shots):
        qvm.reset_qvm()
        result = qvm.run_with_configuration(prog, cbits, 1)
        key = result[0]  # Get measurement result as string
        if key in results:
            results[key] += 1
        else:
            results[key] = 1
    
    # Convert to probability distribution
    total = sum(results.values())
    prob_dist = {key: value / total for key, value in results.items()}
    
    qvm.finalize()
    return prob_dist
