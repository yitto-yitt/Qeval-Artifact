# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X

def dj_algorithm(oracle):
    n = oracle.num_qubits
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    prog = QProg()
    prog << X(qubits[n - 1])
    prog << [H(q) for q in qubits]
    prog << oracle
    prog << [H(q) for q in qubits]
    result = qvm.prob_run_dict(prog, qubits[:n - 1])
    total = sum(result.values())
    return {k: v / total for k, v in result.items()} if total > 0 else result
