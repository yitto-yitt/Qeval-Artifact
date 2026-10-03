# EVAL_META: task_id=31, framework=qpanda, class=1
import pyqpanda3.core as pq

def sampler_qiskit():
    if hasattr(pq, "init"):
        pq.init()

    qvm = pq.CPUQVM()
    if hasattr(qvm, "init_qvm"):
        qvm.init_qvm()
    else:
        qvm.init()

    if hasattr(qvm, "set_seed"):
        qvm.set_seed(42)

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) \
         << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])

    if hasattr(qvm, "run_with_configuration"):
        counts = qvm.run_with_configuration(prog, c, 1024)
    else:
        counts = qvm.runWithConfiguration(prog, c, 1024)

    total = sum(counts.values())
    result = {key: value / total for key, value in counts.items()}

    if hasattr(qvm, "finalize_qvm"):
        qvm.finalize_qvm()
    else:
        qvm.finalize()

    if hasattr(pq, "finalize"):
        pq.finalize()

    return result
