# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = init_quantum_machine(QMachineType.CPU)
    q = qvm.qAlloc_many(n)
    c = qvm.cAlloc_many(n - 1)
    
    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
        
    if callable(oracle):
        prog << oracle(q)
    else:
        prog << oracle
        
    for i in range(n):
        prog << H(q[i])
        
    for i in range(n - 1):
        prog << Measure(q[i], c[i])
        
    result = run_with_configuration(prog, c, shots=1024)
    total = builtins.sum(result.values())
    
    return {key: value / total for key, value in result.items()}
