# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    qm = QMachine()
    qm.init_qubit(2)
    counts = qm.run(qc, 10)
    
    total = sum(counts.values())
    probs = {}
    for k, v in counts.items():
        key_str = k if isinstance(k, str) else f"{k:02b}"
        probs[key_str] = v / total
        
    return probs
