# EVAL_META: task_id=53, framework=qpanda, class=1
import pyqpanda3.core as core

def xor_gate(a, b):
    QMachine = getattr(core, 'QMachine', getattr(core, 'QuantumMachine', None))
    qm = QMachine()
    qubits = qm.allocate_qubits(8)
    circ = core.QuantumCircuit(qubits)
    
    for i in range(8):
        if (a >> i) & 1:
            circ.x(qubits[i])
        if (b >> i) & 1:
            circ.x(qubits[i])
            
    circ.measure_all()
    counts = qm.run(circ, 1000)
    
    if hasattr(counts, 'get_counts'):
        counts = counts.get_counts()
    elif hasattr(counts, 'data') and hasattr(counts.data, 'meas'):
        counts = counts.data.meas.get_counts()
    elif isinstance(counts, list):
        from collections import Counter
        counts = dict(Counter(counts))
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
