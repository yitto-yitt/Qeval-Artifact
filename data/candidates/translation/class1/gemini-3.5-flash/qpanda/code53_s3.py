# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as pq

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    prog = pq.QProg()
    
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            prog.insert(pq.X(q[i]))
            
    for i in range(8):
        prog.insert(pq.Measure(q[i], c[i]))
    
    result = machine.run_with_configuration(prog, c, 1000)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
