# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    for i in range(2):
        qc.measure(i, i)
        
    machine = QMachine()
    counts = machine.run(qc, 1000)
    
    total = sum(counts.values())
    probs = {}
    for k, v in counts.items():
        if isinstance(k, int):
            key = f"{k:02b}"
        else:
            key = str(k)
        probs[key] = v / total
    return probs
