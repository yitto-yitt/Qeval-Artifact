# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def dj_algorithm(oracle):
    n = oracle.get_max_qubit_addr() + 1
    shots = 1024

    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n)
    c = machine.cAlloc_many(n - 1)

    prog = pq.QProg()
    prog << pq.X(q[n - 1])

    for i in range(n):
        prog << pq.H(q[i])

    prog << oracle

    for i in range(n):
        prog << pq.H(q[i])

    for i in range(n - 1):
        prog << pq.Measure(q[i], c[i])

    counts = machine.run_with_configuration(prog, c, shots)

    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    machine.finalize()
    return probs
