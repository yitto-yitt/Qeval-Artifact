# EVAL_META: task_id=56, framework=qpanda2, class=1
import builtins
from pyqpanda import *
def not_gate(a):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7-i] == "0":
            prog.insert(X(qubits[i]))
    for i in range(8):
        prog.insert(Measure(qubits[i], cbits[i]))
    shots = 1024
    result = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(result.values())
    return {key: val / total for key, val in result.items()}
