# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit

def xor_gate(a, b):
    qc = QuantumCircuit(8, 8)
    val = a ^ b
    for i in range(8):
        if (val >> i) & 1:
            qc.x(i)
    qc.measure_all()
    
    try:
        from pyqpanda3.core import Simulator
        sim = Simulator()
    except ImportError:
        from pyqpanda3.simulator import Simulator
        sim = Simulator()
        
    try:
        counts = sim.sampling(qc, 1000)
    except AttributeError:
        counts = sim.run(qc, 1000)
        
    if not isinstance(counts, dict):
        if hasattr(counts, 'get_counts'):
            counts = counts.get_counts()
        elif hasattr(counts, 'counts'):
            counts = counts.counts
            
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
