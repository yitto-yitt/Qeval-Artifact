# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def visualize_bell_states():
    qc_plus = QuantumCircuit(2, 2)
    qc_plus.h(0)
    qc_plus.cx(0, 1)
    for i in range(2):
        qc_plus.measure(i, i)
        
    qc_minus = QuantumCircuit(2, 2)
    qc_minus.x(0)
    qc_minus.h(0)
    qc_minus.cx(0, 1)
    for i in range(2):
        qc_minus.measure(i, i)
        
    qm_plus = QMachine()
    qm_plus.init_qmachine(qc_plus)
    counts_plus = qm_plus.run(qc_plus, 1000)
    
    qm_minus = QMachine()
    qm_minus.init_qmachine(qc_minus)
    counts_minus = qm_minus.run(qc_minus, 1000)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()}
    }
