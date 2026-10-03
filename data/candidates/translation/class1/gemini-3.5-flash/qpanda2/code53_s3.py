# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    # Apply X to q[i] if i-th bit of a is 1
    for i in range(8):
        if (a >> i) & 1:
            prog.insert(pq.X(q[i]))
            
    # Apply X to q[i] if i-th bit of b is 1
    for i in range(8):
        if (b >> i) & 1:
            prog.insert(pq.X(q[i]))
            
    # Measure each qubit to its corresponding classical bit
    for i in range(8):
        prog.insert(pq.Measure(q[i], c[i]))
        
    shots = 1000
    result = machine.run_with_configuration(prog, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
