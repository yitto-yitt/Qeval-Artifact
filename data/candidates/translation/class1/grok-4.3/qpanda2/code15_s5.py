# EVAL_META: task_id=15, framework=qpanda2, class=1
import pyqpanda as pq
import builtins

def noisy_bell():
    machine = pq.NoiseQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    counts = machine.run_with_configuration(prog, 1000)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
