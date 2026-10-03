# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, CNOT, measure

def sampler_qiskit():
    qvm = CPUQVM()
    qubits = range(2)

    prog = QProg()
    prog << H(0)
    prog << CNOT(0, 1)
    for q in qubits:
        prog << measure(q, q)

    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
