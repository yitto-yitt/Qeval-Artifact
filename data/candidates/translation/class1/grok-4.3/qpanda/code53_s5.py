# EVAL_META: task_id=53, framework=qpanda, class=1
from pyqpanda3.core import *
def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if a & (1 << i):
            prog << X(qubits[i])
        if b & (1 << i):
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)
    result = qvm.run_with_configuration(prog, cbits, shots=1024)
    total = sum(result.values())
    return {key: val / total for key, val in result.items()}
