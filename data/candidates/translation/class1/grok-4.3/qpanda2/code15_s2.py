# EVAL_META: task_id=15, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def noisy_bell():
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(2)
    cbits = qvm.cAlloc_many(2)
    prog = QProg()
    prog << H(qubits[0]) << CNOT(qubits[0], qubits[1]) << measure_all(qubits, cbits)
    shots = 1000
    result = qvm.run_with_configuration(prog, cbits, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
