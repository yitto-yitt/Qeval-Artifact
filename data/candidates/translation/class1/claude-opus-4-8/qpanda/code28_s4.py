# EVAL_META: task_id=28, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, X, CNOT, measure

def visualize_bell_states():
    def run(state):
        qvm = CPUQVM()
        prog = QProg()
        circ = QCircuit()
        if state == "phi_minus":
            circ << X(0)
        circ << H(0)
        circ << CNOT(0, 1)
        prog << circ
        prog << measure(0, 0)
        prog << measure(1, 1)
        qvm.run(prog, 1000)
        counts = qvm.result().get_counts()
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}

    return {
        "phi_plus": run("phi_plus"),
        "phi_minus": run("phi_minus"),
    }
