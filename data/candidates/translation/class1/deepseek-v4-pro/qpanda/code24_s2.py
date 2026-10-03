# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import *

def dj_algorithm(oracle):
    init(QMachineType.CPU)

    if hasattr(oracle, 'get_qubits'):
        q = oracle.get_qubits()
        n = len(q)
    else:
        n = oracle.num_qubits if hasattr(oracle, 'num_qubits') else oracle.get_qubit_count()
        q = qalloc(n)
        if callable(oracle):
            oracle = oracle(q)

    c = c_alloc(n - 1)
    prog = QProg()

    prog << X(q[n - 1])
    for i in range(n):
        prog << H(q[i])
    prog << oracle
    for i in range(n):
        prog << H(q[i])
    for i in range(n - 1):
        prog << Measure(q[i], c[i])

    counts = run_with_configuration(prog, c, 1024)
    total = sum(counts.values())
    return {key[::-1]: value / total for key, value in counts.items()}

