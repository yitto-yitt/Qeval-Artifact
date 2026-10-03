# EVAL_META: task_id=31, framework=qpanda2, class=1
import pyqpanda as pq
import builtins
from typing import Dict

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.measure(q[0], c[0]) << pq.measure(q[1], c[1])
    machine.set_random_seed(42)
    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
