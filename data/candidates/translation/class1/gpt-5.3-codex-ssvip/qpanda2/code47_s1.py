# EVAL_META: task_id=47, framework=qpanda2, class=1
import pyqpanda as pq

def random_coin_flip(samples):
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.Measure(q[0], c[0]))

    counts = machine.run_with_configuration(prog, c, samples)

    machine.finalize()

    total = samples if samples > 0 else 1
    heads = counts.get('0', 0) / total
    tails = counts.get('1', 0) / total

    return {'Heads': heads, 'Tails': tails}
