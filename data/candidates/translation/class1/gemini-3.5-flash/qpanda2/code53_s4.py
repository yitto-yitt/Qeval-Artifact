# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    for i in range(8):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        if bit_a:
            prog.insert(pq.X(q[i]))
        if bit_b:
            prog.insert(pq.X(q[i]))
            
    for i in range(8):
        prog.insert(pq.Measure(q[i], c[i]))
        
    shots = 1000
    result = machine.run_with_configuration(prog, c, shots)
    
    total_shots = builtins.sum(result.values())
    prob_dist = {key: val / total_shots for key, val in result.items()}
    
    machine.finalize()
    return prob_dist
