# EVAL_META: task_id=55, framework=qpanda, class=1
from pyqpanda3.core import *
def or_gate(a, b):
    machine = QuantumMachine()
    qubits = machine.allocate_qubits(9)
    cbits = machine.allocate_cbits(3)
    qa = qubits[:3]
    qb = qubits[3:6]
    anc = qubits[6:9]
    prog = QProg()
    a_bin = format(a, '03b')
    b_bin = format(b, '03b')
    for i in range(3):
        if a_bin[2-i] == '0':
            prog << X(qa[i])
        if b_bin[2-i] == '0':
            prog << X(qb[i])
    for i in range(3):
        prog << CCX(qa[i], qb[i], anc[i])
    for i in range(3):
        prog << X(anc[i])
    for i in range(3):
        prog << Measure(anc[i], cbits[i])
    result = machine.run(prog, shots=1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
