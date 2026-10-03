# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def dj_algorithm(oracle):
    qubits = pq.get_all_used_qubits(oracle)
    qubits = sorted(qubits, key=lambda q: q.get_phy_addr())
    n = len(qubits)
    
    cbits = pq.cAlloc_many(n - 1)
    
    prog = pq.QProg()
    prog << pq.X(qubits[-1])
    for q in qubits:
        prog << pq.H(q)
    prog << oracle
    for q in qubits:
        prog << pq.H(q)
        
    for i in range(n - 1):
        prog << pq.Measure(qubits[i], cbits[i])
        
    shots = 1000
    counts = pq.run_with_configuration(prog, cbits, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
