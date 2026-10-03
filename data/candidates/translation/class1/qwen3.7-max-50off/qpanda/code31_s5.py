# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def sampler_qiskit():
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    machine = QMachine()
    if hasattr(machine, 'set_seed'):
        machine.set_seed(42)
        
    result = machine.run(qc, 4000)
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
