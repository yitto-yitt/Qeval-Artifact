# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
from pyqpanda3.core import CPUQVM, QProg, H, CNOT, measure_all

def sampler_qiskit():
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)
    prog = QProg()
    prog << H(q[0]) << CNOT(q[0], q[1])
    prog << measure_all(q, c)
    machine.set_random_seed(42)
    result = machine.run_with_configuration(prog, c, shots=1024)
    counts = result.get_counts()
    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
