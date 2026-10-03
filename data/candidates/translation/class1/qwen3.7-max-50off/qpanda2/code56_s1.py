# EVAL_META: task_id=56, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def not_gate(a):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    
    a_str = format(a, "08b")
    prog = pq.QProg()
    
    for i in range(8):
        if a_str[7-i] == '0':
            prog << pq.X(qubits[i])
            
    for i in range(8):
        prog << pq.Measure(qubits[i], cbits[i])
        
    result = qvm.run_with_configuration(prog, cbits, 1000)
    
    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
