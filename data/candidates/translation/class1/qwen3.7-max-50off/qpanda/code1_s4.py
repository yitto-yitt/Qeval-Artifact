# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QuantumCircuit

def run_bell_state_simulator():
    qm = QMachine()
    q = qm.qAlloc_many(2)
    c = qm.cAlloc_many(2)
    circ = QuantumCircuit(q, c)
    circ.h(q[0])
    circ.cx(q[0], q[1])
    circ.measure(q, c)
    counts = qm.run(circ, 1000)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}
