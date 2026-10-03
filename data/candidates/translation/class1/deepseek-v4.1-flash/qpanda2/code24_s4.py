# EVAL_META: task_id=24, framework=qpanda2, class=1
import builtins
from pyqpanda import *


def dj_algorithm(oracle):
    n = len(oracle.get_used_qubits())

    machine = CPUQVM()
    machine.init_qvm()

    q = machine.qAlloc_many(n)
    c = machine.cAlloc_many(n - 1)

    prog = QProg()
    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])

    prog << oracle

    for i in range(n):
        prog << H(q[i])
    for i in range(n - 1):
        prog << measure(q[i], c[i])

    shots = 1024
    result = machine.run_with_configuration(prog, c, shots)
    machine.finalize()

    total = builtins.sum(result.values())
    return {key: value / total for key, value in result.items()}
