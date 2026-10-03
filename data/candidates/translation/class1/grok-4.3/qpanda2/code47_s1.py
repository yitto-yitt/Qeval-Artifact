# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)
    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.Measure(q[0], c[0]))
    counts = machine.run_with_configuration(prog, c, samples)
    total = builtins.sum(counts.values())
    return {'Heads': counts.get(0, 0) / total, 'Tails': counts.get(1, 0) / total}
