# EVAL_META: task_id=47, framework=qpanda2, class=1
from pyqpanda import init, destroy_quantum_machine, QMachineType, QProg, qAlloc_many, cAlloc_many, H, Measure, run_with_configuration

def random_coin_flip(samples):
    init(QMachineType.CPU)
    q = qAlloc_many(1)
    c = cAlloc_many(1)
    prog = QProg()
    prog << H(q[0])
    prog << Measure(q[0], c[0])
    counts = run_with_configuration(prog, c, samples)
    total = samples
    result = {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total
    }
    destroy_quantum_machine()
    return result
