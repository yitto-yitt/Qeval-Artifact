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
        key = result[0]
        # Convert to binary string format similar to Qiskit
        # Reverse the order to match Qiskit's convention (qubit 1, qubit 0)
        key_reversed = key[::-1] if len(key) == 2 else key.zfill(2)[::-1]
        results[key_reversed] = results.get(key_reversed, 0) + 1
    
    # Calculate probabilities
    total = sum(results.values())
    prob_dist = {key: value / total for key, value in results.items()}
    
    qvm.finalize()
    
    return prob_dist
