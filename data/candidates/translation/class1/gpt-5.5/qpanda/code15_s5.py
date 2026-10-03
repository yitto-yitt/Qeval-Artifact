# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *


def noisy_bell():
    qvm = CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    elif hasattr(qvm, "init"):
        qvm.init()

    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])

    try:
        prog << measure_all(qubits, cbits)
    except NameError:
        prog << Measure(qubits[0], cbits[0])
        prog << Measure(qubits[1], cbits[1])

    counts = qvm.run_with_configuration(prog, cbits, 1000)
    total = sum(counts.values())
    return {str(key): value / total for key, value in counts.items()}
