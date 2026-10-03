# EVAL_META: task_id=31, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure

def sampler_qiskit():
    qvm = CPUQVM()
    qvm.initQVM()
    qvm.set_random_seed(42)
    q = qvm.qAllocMany(2)
    c = qvm.cAllocMany(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << measure(q[0], c[0]) << measure(q[1], c[1])
    counts = qvm.run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
