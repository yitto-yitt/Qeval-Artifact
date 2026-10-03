# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, H, Measure

def random_coin_flip(samples):
    machine = QuantumMachine()
    q = machine.qAlloc_many(1)
    c = machine.cAlloc_many(1)

    prog = QProg()
    prog << H(q[0]) << Measure(q[0], c[0])

    counts = machine.run_with_configuration(prog, c, shots=samples)
    total = sum(counts.values())

    return {
        'Heads': counts.get('0', 0) / total,
        'Tails': counts.get('1', 0) / total,
    }
