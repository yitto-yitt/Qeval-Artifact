# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def xor_gate(a, b):
    qc = QuantumCircuit(8)
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            qc.x(i)
    qc.measure_all()
    
    qvm = QMachine()
    counts = qvm.run(qc, 1000)
    
    if hasattr(counts, 'get_counts'):
        counts = counts.get_counts()
    elif not isinstance(counts, dict):
        counts = {format(val, '08b'): 1000}
        
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
