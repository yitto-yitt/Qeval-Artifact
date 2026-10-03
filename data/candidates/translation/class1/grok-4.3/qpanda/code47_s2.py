# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, Measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(1)
    cbits = qvm.cAlloc_many(1)
    prog = QProg()
    prog << H(qubits[0]) << Measure(qubits[0], cbits[0])
    result = qvm.run_with_configuration(prog, cbits, samples)
    total = sum(result.values())
    return {'Heads': result.get('0', 0) / total, 'Tails': result.get('1', 0) / total}
