# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, CNOT, Measure

def noisy_bell():
    qm = QMachine()
    q = qm.qAlloc(2)
    c = qm.cAlloc(2)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    result = qm.run(prog, 1000)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
