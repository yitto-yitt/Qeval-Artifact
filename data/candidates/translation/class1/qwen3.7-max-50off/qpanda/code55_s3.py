# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QuantumCircuit

def or_gate(a, b):
    qm = QuantumMachine()
    qr_a = qm.qAlloc(3)
    qr_b = qm.qAlloc(3)
    anc = qm.qAlloc(3)
    cr = qm.cAlloc(3)
    
    qc = QuantumCircuit()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            qc.x(qr_a[i])
        if b_bin[2-i] == '0':
            qc.x(qr_b[i])
            
    for i in range(3):
        qc.ccx(qr_a[i], qr_b[i], anc[i])
        
    for i in range(3):
        qc.x(anc[i])
        
    for i in range(3):
        qc.measure(anc[i], cr[i])
        
    counts = qm.run_circuit(qc, shots=10000)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
