# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit
from pyqpanda3.core.simulator import Simulator

def noisy_bell():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    
    sim = Simulator()
    result = sim.run(qc, shots=1000)
    counts = result.get_counts()
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
