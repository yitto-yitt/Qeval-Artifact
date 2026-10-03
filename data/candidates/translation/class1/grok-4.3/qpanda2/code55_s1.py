# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(9)
    cbits = qvm.cAlloc_many(3)
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << X(qubits[i])
        if b_bin[2-i] == '0':
            prog << X(qubits[3+i])
    for i in range(3):
        prog << CCNOT(qubits[i], qubits[3+i], qubits[6+i])
    for i in range(3):
        prog << X(qubits[6+i])
    prog << measure_all(qubits[6:9], cbits)
    shots = 1024
    result = qvm.run_with_configuration(prog, shots)
    counts = result
    total = builtins.sum(counts.values())
    return {k: v / total for k, v in counts.items()}
