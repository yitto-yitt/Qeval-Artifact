# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def not_gate(a):
    machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    q = machine.qAlloc(8)
    c = machine.cAlloc(8)
    
    a_bin = format(a, "08b")
    
    prog = pq.QProg()
    for i in range(8):
        if a_bin[7-i] == '0':
            prog << pq.X(q[i])
            
    for i in range(8):
        prog << pq.Measure(q[i], c[i])
        
    shots = 1000
    counts = machine.run_with_configuration(prog, c, shots)
    
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
