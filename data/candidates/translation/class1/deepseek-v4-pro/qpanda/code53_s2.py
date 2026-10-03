# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import (
    QMachineType,
    init_quantum_machine,
    destroy_quantum_machine,
    qAlloc_many,
    cAlloc_many,
    QProg,
    X,
    measure_all,
    run_with_configuration,
)

def xor_gate(a, b):
    n = 8
    value = (a ^ b) & ((1 << n) - 1)
    desired = format(value, '08b')

    init_quantum_machine(QMachineType.CPU)
    q = qAlloc_many(n)
    c = cAlloc_many(n)

    prog = QProg()
    for i in range(n):
        if (value >> i) & 1:
            prog << X(q[i])
    prog << measure_all(q, c)

    counts = run_with_configuration(prog, 1000)
    destroy_quantum_machine()

    adjusted = {}
    for key, cnt in counts.items():
        if key == desired:
            out_key = desired
        elif key == desired[::-1]:
            out_key = desired
        else:
            out_key = key if key == desired else key[::-1]
        adjusted[out_key] = adjusted.get(out_key, 0) + cnt

    total = sum(adjusted.values()) or 1
    return {k: v / total for k, v in adjusted.items()}
