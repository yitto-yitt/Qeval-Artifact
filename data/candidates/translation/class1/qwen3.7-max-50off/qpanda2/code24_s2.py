# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_list(n)
    
    prog = pq.QProg()
    prog << pq.X(qubits[n - 1])
    for i in range(n):
        prog << pq.H(qubits[i])
        
    if callable(oracle):
        prog << oracle(qubits)
    else:
        prog << oracle
        
    for i in range(n):
        prog << pq.H(qubits[i])
        
    cbits = qvm.cAlloc_list(n - 1)
    for i in range(n - 1):
        prog << pq.Measure(qubits[i], cbits[i])
        
    counts = qvm.run_with_configuration(prog, cbits, 1024)
    total = builtins.sum(counts.values())
    
    return {key: value / total for key, value in counts.items()}
