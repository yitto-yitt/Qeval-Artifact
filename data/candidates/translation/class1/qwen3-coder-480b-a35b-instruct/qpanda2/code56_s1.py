# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import numpy as np

def not_gate(a):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(8)
    
    a = format(a, "08b")
    prog = pq.QProg()
    
    for i in range(8):
        if a[7-i] == "0":
            prog << pq.X(qubits[i])
    
    prog << pq.Measure.all(qubits, pq.QVec())
    
    result = machine.run_with_configuration(prog, shots=1024)
    machine.finalize()
    
    # Calculate total shots
    total = sum(result.values())
    
    # Normalize the counts to get probabilities
    prob_dist = {}
    for key, value in result.items():
        prob_dist[key] = value / total
    
    return prob_dist
