# EVAL_META: task_id=53, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def xor_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(8)
    c = machine.cAlloc_many(8)
    
    prog = pq.QProg()
    
    # Apply X gates for a
    for i in range(8):
        if (a >> i) & 1:
            prog << pq.X(q[i])
            
    # Apply X gates for b
    for i in range(8):
        if (b >> i) & 1:
            prog << pq.X(q[i])
            
    # Measure qubits
    for i in range(8):
        prog << pq.MEASURE(q[i], c[i])
        
    # Run configuration with MSB first (c[7] to c[0])
    shots = 1000
    c_list = [c[i] for i in reversed(range(8))]
    result = machine.run_with_configuration(prog, c_list, shots)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
