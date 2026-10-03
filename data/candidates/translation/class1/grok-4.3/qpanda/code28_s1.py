# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QuantumCircuit, simulate

def visualize_bell_states():
    phi_plus = QuantumCircuit(2)
    phi_minus = QuantumCircuit(2)
    phi_plus.h(0)
    phi_plus.cx(0, 1)
    phi_minus.x(0)
    phi_minus.h(0)
    phi_minus.cx(0, 1)
    phi_plus.measure_all()
    phi_minus.measure_all()
    result_phi_plus = simulate(phi_plus, shots=1000)
    result_phi_minus = simulate(phi_minus, shots=1000)
    phi_plus_counts = result_phi_plus.get_counts()
    phi_minus_counts = result_phi_minus.get_counts()
    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())
    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
