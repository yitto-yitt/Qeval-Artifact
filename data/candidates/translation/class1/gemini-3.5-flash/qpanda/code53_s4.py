# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

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
    
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
