# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure


def visualize_bell_states():
    distributions = {}
    for name in ("phi_plus", "phi_minus"):
        program = QProg()
        if name == "phi_minus":
            program << X(0)
        program << H(0) << CNOT(0, 1)
        program << measure(0, 0) << measure(1, 1)

        simulator = CPUQVM()
        simulator.run(program, 1000)
        counts = simulator.result().get_counts()
        total = sum(counts.values())
        distributions[name] = {
            bits: count / total for bits, count in counts.items()
        }

    return distributions
