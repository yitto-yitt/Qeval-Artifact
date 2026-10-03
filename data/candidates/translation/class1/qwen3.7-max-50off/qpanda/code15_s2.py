# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    machine = QMachine()
    counts = machine.run(qc, 1000)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
