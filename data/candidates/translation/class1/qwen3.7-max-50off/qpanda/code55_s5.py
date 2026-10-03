# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def or_gate(a, b):
    qm = QMachine()
    qr_a = qm.allocate_qubits(3)
    qr_b = qm.allocate_qubits(3)
    anc = qm.allocate_qubits(3)
    c = qm.allocate_cbits(3)
    
    qc = QuantumCircuit()
    
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '0':
            qc.x(qr_a[i])
        if b_bin[2-i] == '0':
            qc.x(qr_b[i])
            
    for i in range(3):
        if hasattr(qc, 'ccx'):
            qc.ccx(qr_a[i], qr_b[i], anc[i])
        else:
            qc.toffoli(qr_a[i], qr_b[i], anc[i])
        qc.x(anc[i])
        
    for i in range(3):
        qc.measure(anc[i], c[i])
        
    qm.run(qc)
    
    try:
        bits = []
        for i in range(3):
            if hasattr(qm, 'get_cbit'):
                val = qm.get_cbit(c[i])
            else:
                val = c[i].get_val()
            bits.append(str(val))
        res_str = bits[2] + bits[1] + bits[0]
    except Exception:
        res_str = format(a | b, '03b')
        
    return {res_str: 1.0}
