# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubit = qvm.qAlloc()
    cbit = qvm.cAlloc()
    prog = QProg()
    prog << H(qubit) << Measure(qubit, cbit)
    result = qvm.run_with_configuration(prog, [cbit], samples)
    total = sum(result.values())
    return {'Heads': result.get('0', 0) / total, 'Tails': result.get('1', 0) / total}
