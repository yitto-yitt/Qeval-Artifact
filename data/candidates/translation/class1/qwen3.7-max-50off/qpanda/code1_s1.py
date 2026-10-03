# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def run_bell_state_simulator():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    qm = QMachine()
    try:
        qm.init_qmachine(2, 2)
    except Exception:
        pass
        
    result = qm.run(qc, 1000)
    counts = result.get_counts()
    
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
