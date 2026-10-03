# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, X, measure_all

def not_gate(a):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    a = format(a, "08b")
    prog = QProg()
    for i in range(8):
        if a[7 - i] == "0":
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)
    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
