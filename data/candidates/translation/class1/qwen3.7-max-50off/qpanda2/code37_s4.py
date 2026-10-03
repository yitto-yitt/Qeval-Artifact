# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def bv_algorithm(s):
    n = len(s)
    qvm = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = qvm.qAlloc_many(n + 1)
    c = qvm.cAlloc_many(n)
    
    prog = pq.QProg()
    ancilla = n
    
    prog << pq.X(q[ancilla])
    for i in range(n + 1):
        prog << pq.H(q[i])
        
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(q[index], q[ancilla])
            
    for i in range(n):
        prog << pq.H(q[i])
        
    for i in range(n):
        prog << pq.Measure(q[i], c[i])
        
    result = pq.run_with_configuration(prog, c, 1)
    bitstrings = list(result.keys())
    
    return [bitstrings, result]
