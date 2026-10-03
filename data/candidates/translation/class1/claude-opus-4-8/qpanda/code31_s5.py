# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, CNOT, measure

def sampler_qiskit():
    qc = QProg()
    circuit = QCircuit(2)
    circuit << H(0)
    circuit << CNOT(0, 1)
    qc << circuit
    qc << measure(0, 0)
    qc << measure(1, 1)

    qvm = CPUQVM()
    qvm.run(qc, 1024)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
