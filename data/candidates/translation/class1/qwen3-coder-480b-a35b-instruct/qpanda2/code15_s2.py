# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def noisy_bell():
    # Create quantum circuit equivalent to Bell state
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    qubits = machine.qAlloc_many(2)
    cbits = machine.cAlloc_many(2)
    
    prog = pq.QProg()
    prog.insert(pq.H(qubits[0]))
    prog.insert(pq.CNOT(qubits[0], qubits[1]))
    prog.insert(pq.Measure(qubits[0], cbits[0]))
    prog.insert(pq.Measure(qubits[1], cbits[1]))
    
    # Run the program
    result = machine.run(prog)
    
    # Get the count results
    counts = result
    total_shots = 1000
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in counts.items():
        prob_dist[key] = value / total_shots
        
    machine.destroy_qvm()
    return prob_dist
