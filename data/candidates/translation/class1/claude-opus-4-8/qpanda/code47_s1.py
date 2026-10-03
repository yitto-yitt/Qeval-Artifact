# EVAL_META: task_id=47, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, QCircuit, H, measure

def random_coin_flip(samples):
    qvm = CPUQVM()
    prog = QProg()
    circuit = QCircuit()
    circuit << H(0)
    prog << circuit
    prog << measure(0, 0)
    qvm.run(prog, samples)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    heads = counts.get('0', 0)
    tails = counts.get('1', 0)
    return {'Heads': heads / total, 'Tails': tails / total}
