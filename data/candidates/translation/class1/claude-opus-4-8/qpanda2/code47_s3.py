# EVAL_META: task_id=47, framework=qpanda2, class=1
import builtins
from pyqpanda import CPUQVM, H, measure_all

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    prog = qvm.qCreateEmptyQProg() if hasattr(qvm, "qCreateEmptyQProg") else None
    from pyqpanda import QProg
    prog = QProg()
    prog << H(qubits[0]) << measure_all(qubits, cbits)
    counts = qvm.run_with_configuration(prog, cbits, samples)
    total = builtins.sum(counts.values())
    heads = counts.get('0', 0)
    tails = counts.get('1', 0)
    qvm.finalize()
    return {'Heads': heads / total, 'Tails': tails / total}
