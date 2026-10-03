# EVAL_META: task_id=31, framework=qpanda2, class=1
from typing import Dict
import builtins
from pyqpanda import (
    QProg,
    H,
    CNOT,
    measure,
    CPUQVM,
    init_quantum_machine,
    qAlloc_many,
    cAlloc_many,
)


def sampler_qiskit():
    machine = CPUQVM()
    machine.init_qvm()

    q = qAlloc_many(2)
    c = cAlloc_many(2)

    prog = QProg()
    prog << H(q[0])
    prog << CNOT(q[0], q[1])
    prog << measure(q[0], c[0])
    prog << measure(q[1], c[1])

    shots = 1024
    counts = machine.run_with_configuration(prog, c, shots)

    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
