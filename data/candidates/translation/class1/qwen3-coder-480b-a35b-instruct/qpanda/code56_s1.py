# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda import *
from collections import defaultdict

def not_gate(a):
    a = format(a, "08b")
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if a[7-i] == "0":
            prog.insert(X(qubits[i]))
    for i in range(8):
        prog.insert(MEASURE(qubits[i], cbits[i]))
    result = qvm.run_with_configuration(prog, cbits, 1000)
    qvm.finalize()
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
