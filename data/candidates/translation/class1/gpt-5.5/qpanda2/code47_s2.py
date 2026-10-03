# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
import pyqpanda as pq

def random_coin_flip(samples):
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    try:
        q = qvm.qAlloc_many(1)
        c = qvm.cAlloc_many(1)

        prog = pq.QProg()
        prog << pq.H(q[0]) << pq.Measure(q[0], c[0])

        counts = qvm.run_with_configuration(prog, c, samples)
        total = builtins.sum(counts.values())

        return {
            'Heads': counts.get('0', 0) / total,
            'Tails': counts.get('1', 0) / total
        }
    finally:
        qvm.finalize()
