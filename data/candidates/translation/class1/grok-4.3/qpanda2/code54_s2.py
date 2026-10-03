# EVAL_META: task_id=54, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def and_gate(a, b):
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(9)
    cbits = machine.cAlloc_many(3)
    q_a = qubits[0:3]
    q_b = qubits[3:6]
    anc = qubits[6:9]
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2 - i] == '1':
            prog << X(q_a[i])
        if b_bin[2 - i] == '1':
            prog << X(q_b[i])
    for i in range(3):
        prog << Toffoli(q_a[i], q_b[i], anc[i])
    for i in range(3):
        prog << Measure(anc[i], cbits[i])
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
