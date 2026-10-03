# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
from pyqpanda import *
import numpy as np

def noisy_bell():
    # Initialize QVM
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    
    # Create Bell circuit
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    # Run the program
    result = run_with_configuration(machine, prog, c, 1000)
    
    # Calculate total shots
    import builtins
    total_shots = builtins.sum(result.values())
    
    # Convert to probability distribution
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total_shots
    
    destroy_quantum_machine(machine)
    return prob_dist
