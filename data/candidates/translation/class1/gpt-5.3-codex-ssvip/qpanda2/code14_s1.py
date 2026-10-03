# EVAL_META: task_id=14, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def bell_each_shot():
    shots = 10
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)

    counts = run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    destroy_quantum_machine(machine)

    return {k: v / total for k, v in counts.items()}
