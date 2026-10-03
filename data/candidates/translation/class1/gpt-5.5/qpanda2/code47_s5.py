# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    try:
        qubit = qvm.qAlloc()
        cbit = qvm.cAlloc()

        prog = QProg()
        prog << H(qubit) << Measure(qubit, cbit)

        counts = qvm.run_with_configuration(prog, [cbit], samples)
        total = builtins.sum(counts.values())

        return {
            'Heads': counts.get('0', 0) / total,
            'Tails': counts.get('1', 0) / total
        }
    finally:
        qvm.finalize()
