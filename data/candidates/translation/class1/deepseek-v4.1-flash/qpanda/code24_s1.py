# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, measure, CBit

def dj_algorithm(oracle):
    qubits = oracle.get_used_qubits()
    qubits = sorted(qubits, key=lambda q: q.get_id())
    n = len(qubits)
    input_qubits = qubits[:n - 1]
    output_qubit = qubits[n - 1]

    qvm = CPUQVM()
    qvm.init_qvm()
    cbits = [CBit(i) for i in range(n - 1)]

    prog = QProg()
    prog << X(output_qubit)
    for q in qubits:
        prog << H(q)
    prog << oracle
    for q in qubits:
        prog << H(q)
    for i in range(n - 1):
        prog << measure(input_qubits[i], cbits[i])

    result = qvm.prob_run_dict(prog, list(reversed(cbits)))
    qvm.finalize()
    return result
