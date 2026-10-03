# EVAL_META: task_id=14, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, CNOT, Measure

def bell_each_shot():
    qm = QMachine()
    q = qm.qAlloc(2)
    c = qm.cAlloc(2)
    
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    
    counts = qm.run(prog, 10)
    
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
