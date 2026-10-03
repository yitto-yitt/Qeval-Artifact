# EVAL_META: task_id=55, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def or_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    a_qubits = qvm.qAlloc_many(3)
    b_qubits = qvm.qAlloc_many(3)
    anc = qvm.qAlloc_many(3)
    c = qvm.cAlloc_many(3)
    prog = QProg()
    a_str = format(a, '03b')
    b_str = format(b, '03b')
    for i in range(3):
        if a_str[2-i] == '0':
            prog << X(a_qubits[i])
        if b_str[2-i] == '0':
            prog << X(b_qubits[i])
    for i in range(3):
        prog << Toffoli(a_qubits[i], b_qubits[i], anc[i])
    for i in range(3):
        prog << X(anc[i])
    for i in range(3):
        prog << Measure(anc[i], c[i])
    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)
    total = builtins.sum(result.values())
    prob_dist = {key: value / total for key, value in result.items()}
    qvm.finalize()
    return prob_dist
