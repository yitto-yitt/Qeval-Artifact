# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *

def noisy_bell():
    init(QMachineType.CPU)
    try:
        qubits = qAlloc_many(2)
        cbits = cAlloc_many(2)

        prog = QProg()
        prog << H(qubits[0]) << CNOT(qubits[0], qubits[1])
        prog << Measure(qubits[0], cbits[0]) << Measure(qubits[1], cbits[1])

        counts = run_with_configuration(prog, cbits, 1000)
        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        finalize()
