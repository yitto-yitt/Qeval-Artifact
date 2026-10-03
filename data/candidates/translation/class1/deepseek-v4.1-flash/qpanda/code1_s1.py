# EVAL_META: task_id=1, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, Measure

def run_bell_state_simulator():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << Measure(q[0], c[0]) << Measure(q[1], c[1])
    counts = machine.run_with_configuration(prog, c, 1000)
    machine.finalize()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        if isinstance(key, int):
            key = format(key, '02b')
        result[key] = value / total
    return result
