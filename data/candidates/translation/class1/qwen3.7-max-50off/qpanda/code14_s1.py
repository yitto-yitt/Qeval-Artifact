# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def bell_each_shot():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    qm = QMachine()
    result = qm.run(qc, 10)
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
