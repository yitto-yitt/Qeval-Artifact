# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def bell_each_shot():
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])

    shots = 10
    counts = machine.run_with_configuration(prog, c, shots)

    total = builtins.sum(counts.values())
    probs = {k: v / total for k, v in counts.items()}

    destroy_quantum_machine(machine)
    return probs
