# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import builtins
from pyqpanda import CPUQVM, QProg, H, CNOT, MeasureAll, destroy_quantum_machine

def sampler_qiskit():
    machine = CPUQVM()
    machine.init_qvm()
    machine.set_random_seed(42)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << MeasureAll(q, c)
    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    result = {key: value / total for key, value in counts.items()}
    destroy_quantum_machine(machine)
    return result
