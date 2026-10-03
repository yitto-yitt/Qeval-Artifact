# EVAL_META: task_id=15, framework=qpanda, class=1
from pyqpanda3.core import *
def noisy_bell():
    machine = NoiseQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    result = machine.run_with_configuration(prog, c, shots=1000)
    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
