# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import QMachine, QProg, H, CNOT, Measure

def run_bell_state_simulator():
    machine = QMachine()
    machine.init()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    counts = machine.run_with_configuration(prog, 1000)
    machine.finalize()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
