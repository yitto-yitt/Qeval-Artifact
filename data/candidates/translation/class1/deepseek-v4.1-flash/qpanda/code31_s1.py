# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def sampler_qiskit():
    qvm = CPUQVM()
    qvm.init_qvm()
    if hasattr(qvm, 'set_random_seed'):
        qvm.set_random_seed(42)
    elif hasattr(qvm, 'set_seed'):
        qvm.set_seed(42)

    q = qvm.qAlloc_many(2)
    c = qvm.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0])
    prog << Measure(q[1], c[1])

    shots = 1024
    result = qvm.run_with_configuration(prog, c, shots)

    counts = {}
    for key, val in result.items():
        try:
            bitstr = format(int(key), '02b')
        except ValueError:
            bitstr = str(key)
        counts[bitstr] = counts.get(bitstr, 0) + val

    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
