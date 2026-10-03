# EVAL_META: task_id=24, framework=qpanda2, class=1
import pyqpanda
import builtins

def dj_algorithm(oracle):
    n = oracle.num_qubits
    
    qvm = pyqpanda.CPUQVM()
    qvm.init()
    q = qvm.qAlloc(n)
    c = qvm.cAlloc(n - 1)
    
    prog = pyqpanda.QProg()
    prog << pyqpanda.X(q[n - 1])
    
    for i in range(n):
        prog << pyqpanda.H(q[i])
        
    prog << oracle
    
    for i in range(n):
        prog << pyqpanda.H(q[i])
        
    for i in range(n - 1):
        prog << pyqpanda.Measure(q[i], c[i])
        
    shots = 1024
    counts = qvm.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
