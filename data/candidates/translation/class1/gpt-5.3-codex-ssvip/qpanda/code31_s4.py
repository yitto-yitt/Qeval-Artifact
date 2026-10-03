# EVAL_META: task_id=31, framework=qpanda, class=1
from typing import Dict
import pyqpanda3.core as pq


def sampler_qiskit():
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(2)
    c = machine.cAlloc_many(2)

    prog = pq.QProg()
    prog.insert(pq.H(q[0]))
    prog.insert(pq.CNOT(q[0], q[1]))
    prog.insert(pq.Measure(q[0], c[0]))
    prog.insert(pq.Measure(q[1], c[1]))

    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = sum(result.values())
    return {k: v / total for k, v in result.items()}
