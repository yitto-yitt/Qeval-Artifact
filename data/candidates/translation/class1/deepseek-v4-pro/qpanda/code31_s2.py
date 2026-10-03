# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import init_qvm, destroy, qAlloc_many, cAlloc_many, QProg, H, CNOT, MeasureAll, run_with_configuration

def sampler_qiskit():
    init_qvm(42)
    q = qAlloc_many(2)
    c = cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)

    counts = run_with_configuration(prog, c, 1024)
    destroy()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
