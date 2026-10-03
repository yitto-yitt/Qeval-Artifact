# EVAL_META: task_id=55, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
def or_gate(a, b):
    machine = pq.CPUQVM()
    machine.init_qvm()
    qa = machine.qAlloc_many(3)
    qb = machine.qAlloc_many(3)
    qanc = machine.qAlloc_many(3)
    c = machine.cAlloc_many(3)
    prog = pq.QProg()
    astr = format(a, '03b')
    bstr = format(b, '03b')
    for i in range(3):
        if astr[2 - i] == '0':
            prog << pq.X(qa[i])
        if bstr[2 - i] == '0':
            prog << pq.X(qb[i])
    for i in range(3):
        prog << pq.Toffoli(qa[i], qb[i], qanc[i])
    for i in range(3):
        prog << pq.X(qanc[i])
    for i in range(3):
        prog << pq.Measure(qanc[i], c[i])
    result = machine.run_with_configuration(prog, shots=1024)
    counts = result
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
