# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, Measure

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if (a >> i) & 1:
            prog << X(qubits[i])
        if (b >> i) & 1:
            prog << X(qubits[i])
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    # reverse keys to get standard binary representation (LSB rightmost)
    prob_dist = {k[::-1]: v / total for k, v in result.items()}
    qvm.finalize_qvm()
    return prob_dist
