# EVAL_META: task_id=31, framework=qpanda2, class=1
import builtins
from typing import Dict
from pyqpanda import *

def sampler_qiskit():
    machine = init_quantum_machine(QMachineType.CPU)
    machine.set_random_seed(42)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1]) << Measure(q[0], c[0]) << Measure(q[1], c[1])
    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    probs = {}
    for key, value in counts.items():
        bitstring = format(key, '02b')
        probs[bitstring] = value / total
    machine.finalize()
    return probs
