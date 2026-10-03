# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure

def bell_each_shot():
    qvm = CPUQVM()

    circ = QCircuit(2)
    circ << H(0)
    circ << CNOT(0, 1)

    prog = QProg()
    prog << circ
    prog << measure(0, 0)
    prog << measure(1, 1)

    qvm.run(prog, 10)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
