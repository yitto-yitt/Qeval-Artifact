# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, measure, X

def not_gate(a):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    a_bin = format(a, "08b")
    for i in range(8):
        if a_bin[7 - i] == "0":
            prog << X(qubits[i])
    for i in range(8):
        prog << measure(qubits[i], cbits[i])
    result = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(result.values())
    return {key: value / total for key, value in result.items()}
