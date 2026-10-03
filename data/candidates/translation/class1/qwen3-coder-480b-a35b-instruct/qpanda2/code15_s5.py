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
    prog.insert(pq.H(qubits[0])) \
        .insert(pq.CNOT(qubits[0], qubits[1])) \
        .insert(pq.Measure(qubits[0], cbits[0])) \
        .insert(pq.Measure(qubits[1], cbits[1]))
    
    # Run the program with specified number of shots
    shots = 1000
    result = machine.run_with_configuration(prog, cbits, shots)
    
    # Calculate total shots
    import builtins
    total = builtins.sum(result.values())
    
    # Normalize counts to probabilities
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total
    
    machine.finalize()
    
    return prob_dist
