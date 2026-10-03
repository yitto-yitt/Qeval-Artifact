# EVAL_META: task_id=54, framework=qpanda, class=1
import pyqpanda3 as pq

def and_gate(a, b):
    qm = pq.QMachine()
    qr_a = qm.qAlloc_vec(3)
    qr_b = qm.qAlloc_vec(3)
    ancillary = qm.qAlloc_vec(3)
    cr = qm.cAlloc_vec(3)
    
    circ = pq.QCircuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            circ << pq.X(qr_a[i])
        if b_bin[2-i] == '1':
            circ << pq.X(qr_b[i])
            
    for i in range(3):
        circ << pq.Toffoli(qr_a[i], qr_b[i], ancillary[i])
        
    for i in range(3):
        circ << pq.Measure(ancillary[i], cr[i])
        
    prog = pq.QProg()
    prog << circ
    
    counts = qm.run_with_configuration(prog, cr, 1000)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
