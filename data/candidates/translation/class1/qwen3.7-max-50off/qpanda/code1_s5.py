# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def run_bell_state_simulator():
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    
    machine = QMachine()
    result = machine.run(qc, 1000)
    
    if hasattr(result, 'get_counts'):
        counts = result.get_counts()
    else:
        counts = result
        
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
