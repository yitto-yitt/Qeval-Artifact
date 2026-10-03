# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, X, CCX, Measure

def and_gate(a, b):
    machine = QuantumMachine()
    q_a = machine.qAlloc(3)
    q_b = machine.qAlloc(3)
    q_anc = machine.qAlloc(3)
    c = machine.cAlloc(3)
    
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            prog << X(q_a[i])
        if b_bin[2-i] == '1':
            prog << X(q_b[i])
            
    for i in range(3):
        prog << CCX(q_a[i], q_b[i], q_anc[i])
        
    for i in range(3):
        prog << Measure(q_anc[i], c[i])
        
    result = machine.run(prog, 10000)
    if hasattr(result, 'get_counts'):
        counts = result.get_counts()
    else:
        counts = result
        
    total = sum(counts.values())
    probs = {}
    for key, value in counts.items():
        k = key if isinstance(key, str) else format(key, '03b')
        probs[k] = value / total
        
    return probs
