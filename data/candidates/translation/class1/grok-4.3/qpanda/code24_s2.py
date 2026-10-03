# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, qAlloc_many, cAlloc_many, X, H, measure
def dj_algorithm(oracle):
    n = oracle.num_qubits
    prog = QProg()
    qv = qAlloc_many(n)
    cv = cAlloc_many(n - 1)
    prog << X(qv[n - 1])
    for i in range(n):
        prog << H(qv[i])
    prog << oracle
    for i in range(n):
        prog << H(qv[i])
    prog << measure(qv[:n - 1], cv)
    machine = CPUQVM()
    machine.init_qvm()
    result = machine.prob_run_dict(prog, cv)
    return result
