# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, QMachine

def visualize_bell_states():
    phi_plus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_plus.measure_all()
    
    phi_minus = QuantumCircuit(2)
    phi_minus.x(0)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_minus.measure_all()
    
    machine = QMachine()
    
    counts_plus = machine.run(phi_plus, 1000)
    counts_minus = machine.run(phi_minus, 1000)
    
    total_plus = sum(counts_plus.values())
    total_minus = sum(counts_minus.values())
    
    return {
        "phi_plus": {k: v / total_plus for k, v in counts_plus.items()},
        "phi_minus": {k: v / total_minus for k, v in counts_minus.items()}
    }
