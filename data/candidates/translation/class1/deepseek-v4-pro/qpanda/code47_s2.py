# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    init = getattr(qvm, 'init_qvm', None) or getattr(qvm, 'initQVM')
    init()
    qalloc = getattr(qvm, 'qalloc_many', None) or getattr(qvm, 'qAlloc_many')
    calloc = getattr(qvm, 'calloc_many', None) or getattr(qvm, 'cAlloc_many')
    qubits = qalloc(1)
    cbits = calloc(1)
    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])
    run = getattr(qvm, 'run_with_configuration', None) or getattr(qvm, 'runWithConfiguration')
    counts = run(prog, cbits, samples)
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
