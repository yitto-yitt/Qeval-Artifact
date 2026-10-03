# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure

def run_bell_state_simulator():
    qvm = CPUQVM()
    prog = QProg()
    prog << H(0)
    prog << CNOT(0, 1)
    prog << measure(0, 0)
    prog << measure(1, 1)
    qvm.run(prog, 1000)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
