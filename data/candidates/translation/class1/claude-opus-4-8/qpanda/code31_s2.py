# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT, measure

def sampler_qiskit():
    qc = QCircuit(2)
    qc << H(0)
    qc << CNOT(0, 1)

    prog = QProg()
    prog << qc
    prog << measure(0, 0)
    prog << measure(1, 1)

    qvm = CPUQVM()
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
