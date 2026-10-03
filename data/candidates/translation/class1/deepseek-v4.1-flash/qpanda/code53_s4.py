# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import QProg, CPUQVM, X, measure

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
    prog << measure(qubits, cbits)

    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
