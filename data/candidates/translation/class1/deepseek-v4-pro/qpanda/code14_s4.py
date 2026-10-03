# EVAL_META: task_id=14, framework=qpanda, class=1
import pyqpanda3.core as pq

def bell_each_shot():
    pq.init()
    try:
        q = pq.qAlloc_many(2)
        c = pq.cAlloc_many(2)
        prog = pq.QProg()
        prog << pq.H(q[0]) << pq.CNOT(q[0], q[1])
        prog << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])

        try:
            counts = pq.run_with_configuration(prog, c, 10)
        except TypeError:
            counts = pq.run_with_configuration(prog, 10)

        total = sum(counts.values())
        return {key: value / total for key, value in counts.items()}
    finally:
        pq.finalize()
