# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure

def run_bell_state_simulator():
    qvm = CPUQVM()
    prog = QProg()
    circ = QCircuit()
    circ << H(0)
    circ << CNOT(0, 1)
    prog << circ
    prog << measure(0, 0)
    prog << measure(1, 1)
    shots = 1000
    qvm.run(prog, shots)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
