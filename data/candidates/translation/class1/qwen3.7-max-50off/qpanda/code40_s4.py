# EVAL_META: task_id=40, framework=qpanda, class=1
from pyqpanda3.core import QuantumMachine, QProg, init_state, Measure

def init_random_3qubit(desired_vector):
    qm = QuantumMachine()
    q = qm.qAlloc_many(3)
    c = qm.cAlloc_many(3)
    prog = QProg()
    prog << init_state(q, desired_vector)
    for i in range(3):
        prog << Measure(q[i], c[i])
    
    counts = qm.run(prog, 4000)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
