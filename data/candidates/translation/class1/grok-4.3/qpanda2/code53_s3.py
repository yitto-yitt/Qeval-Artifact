# EVAL_META: task_id=53, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def xor_gate(a, b):
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    for i in range(8):
        if (a & (1 << i)) != 0:
            prog << X(qubits[i])
        if (b & (1 << i)) != 0:
            prog << X(qubits[i])
    for i in range(8):
        prog << Measure(qubits[i], cbits[i])
    counts = qvm.run_with_configuration(prog, shots=1024)
    prob_dict = {}
    for key, value in counts.items():
        new_key = key[::-1]
        prob_dict[new_key] = prob_dict.get(new_key, 0) + value
    total = builtins.sum(prob_dict.values())
    return {key: value / total for key, value in prob_dict.items()}
