# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(q[i])
        if (b >> i) & 1:
            prog << pq.X(q[i])
            
    for i in range(8):
        prog << pq.Measure(q[i], c[i])
        
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    probs = {}
    for key, val in result.items():
        rev_key = key[::-1]
        if len(rev_key) < 8:
            rev_key = rev_key.zfill(8)
        probs[rev_key] = val / total
        
    return probs
