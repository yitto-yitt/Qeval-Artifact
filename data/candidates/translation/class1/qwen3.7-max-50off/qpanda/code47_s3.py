# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, H, Measure

def random_coin_flip(samples):
    qm = QuantumMachine()
    q = qm.qAlloc_many(1)
    c = qm.cAlloc_many(1)
    prog = QProg()
    prog.insert(H(q[0]))
    prog.insert(Measure(q[0], c[0]))
    counts = qm.run_with_configuration(prog, c, samples)
    total = sum(counts.values())
    return {'Heads': counts.get('0', 0) / total, 'Tails': counts.get('1', 0) / total}
