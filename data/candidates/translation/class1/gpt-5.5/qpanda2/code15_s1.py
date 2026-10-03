# EVAL_META: task_id=15, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, CNOT, Measure

def noisy_bell():
    shots = 1000
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(qubits[0])
    prog << CNOT(qubits[0], qubits[1])
    prog << Measure(qubits[0], cbits[0])
    prog << Measure(qubits[1], cbits[1])

    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    qvm.finalize()
    return {key: value / total for key, value in counts.items()}
