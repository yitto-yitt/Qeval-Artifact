# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq

def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    machine.set_random_seed(42)
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = pq.QProg()
    prog << pq.H(q[0]) << pq.CNOT(q[0], q[1]) << pq.Measure(q[0], c[0]) << pq.Measure(q[1], c[1])
    result = machine.run_with_configuration(prog, cbit_list=c, shots=1024)
    counts = result
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
