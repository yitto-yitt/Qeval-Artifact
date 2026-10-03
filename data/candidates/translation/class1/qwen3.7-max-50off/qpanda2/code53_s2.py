# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    val = a ^ b
    
    for i in range(8):
        if (val >> i) & 1:
            prog << pq.X(q[i])
            
    for i in range(8):
        prog << pq.Measure(q[i], c[i])
        
    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
