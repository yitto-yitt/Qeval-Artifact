# EVAL_META: task_id=47, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    q = qvm.qAlloc_many(1)
    c = qvm.cAlloc_many(1)

    circuit = QCircuit()
    circuit << H(q[0])
    circuit << Measure(q[0], c[0])

    result = qvm.run_with_configuration(circuit, c, samples)
    total = builtins.sum(result.values())
    if total == 0:
        total = samples

    qvm.finalize()
    return {
        'Heads': result.get('0', 0) / total,
        'Tails': result.get('1', 0) / total,
    }
