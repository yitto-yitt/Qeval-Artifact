# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, CNOT, measure

def visualize_bell_states():
    shots = 1000

    phi_plus = QProg()
    phi_plus << H(0)
    phi_plus << CNOT(0, 1)
    phi_plus << measure(0, 0)
    phi_plus << measure(1, 1)

    phi_minus = QProg()
    phi_minus << X(0)
    phi_minus << H(0)
    phi_minus << CNOT(0, 1)
    phi_minus << measure(0, 0)
    phi_minus << measure(1, 1)

    machine = CPUQVM()

    machine.run(phi_plus, shots)
    phi_plus_counts = machine.result().get_counts()

    machine.run(phi_minus, shots)
    phi_minus_counts = machine.result().get_counts()

    phi_plus_total = sum(phi_plus_counts.values())
    phi_minus_total = sum(phi_minus_counts.values())

    return {
        "phi_plus": {key: value / phi_plus_total for key, value in phi_plus_counts.items()},
        "phi_minus": {key: value / phi_minus_total for key, value in phi_minus_counts.items()},
    }
