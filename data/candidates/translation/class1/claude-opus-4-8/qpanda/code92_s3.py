# EVAL_META: task_id=92, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT

def calculate_stabilizer_state_info():
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)

    prog = QProg()
    prog << qc

    qvm = CPUQVM()
    qvm.run(prog, 1000)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    probabilities_dict = {}
    for state, count in counts.items():
        key = state[::-1]
        probabilities_dict[key] = count / total
    return probabilities_dict
