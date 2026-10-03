# EVAL_META: task_id=54, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QuantumMachine

def and_gate(a, b):
    qm = QuantumMachine()
    qa = qm.alloc_qubits(3)
    qb = qm.alloc_qubits(3)
    anc = qm.alloc_qubits(3)
    c = qm.alloc_cbits(3)
    
    qc = QuantumCircuit()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    
    for i in range(3):
        if a_bin[2-i] == '1':
            qc.x(qa[i])
        if b_bin[2-i] == '1':
            qc.x(qb[i])
            
    for i in range(3):
        qc.ccx(qa[i], qb[i], anc[i])
        
    qc.measure(anc, c)
    
    result = qm.run(qc, 1000)
    
    if hasattr(result, 'get_counts'):
        counts = result.get_counts()
    elif hasattr(result, 'counts'):
        counts = result.counts
    else:
        counts = result
        
    formatted_counts = {}
    for k, v in counts.items():
        if isinstance(k, int):
            k_str = format(k, '03b')
        else:
            k_str = str(k)
            if len(k_str) < 3:
                k_str = k_str.zfill(3)
        formatted_counts[k_str] = formatted_counts.get(k_str, 0) + v
        
    total = sum(formatted_counts.values())
    return {key: value / total for key, value in formatted_counts.items()}
