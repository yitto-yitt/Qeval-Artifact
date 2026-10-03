# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3.core as pq

def and_gate(a, b):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)
    
    prog = pq.QProg()
    
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    
    for i in range(3):
        if a_str[2-i] == '1':
            prog.insert(pq.X(qubits[i]))
        if b_str[2-i] == '1':
            prog.insert(pq.X(qubits[3+i]))
            
    for i in range(3):
        prog.insert(pq.X(qubits[6+i]).control([qubits[i], qubits[3+i]]))
        
    for i in range(3):
        prog.insert(pq.Measure(qubits[6+i], cbits[2-i]))
        
    result = qvm.run_with_configuration(prog, cbits, 1000)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
