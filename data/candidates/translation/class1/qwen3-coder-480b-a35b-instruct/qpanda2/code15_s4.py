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
    result = machine.run_with_configuration(prog, cbits, 1000)
    
    # Convert result to probability distribution
    total_shots = 1000
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    machine.finalize()
    return prob_dist
