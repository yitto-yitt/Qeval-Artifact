# EVAL_META: task_id=56, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, X, measure_all

def not_gate(a):
    qvm = CPUQVM()
    qvm.initQVM()
    qubits = qvm.qAlloc_many(8)
    cbits = qvm.cAlloc_many(8)
    prog = QProg()
    a_str = format(a, "08b")
    for i in range(8):
        if a_str[7 - i] == "0":
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)
    counts = qvm.run_with_configuration(prog, cbits, 1024)
    total = sum(counts.values())
    prob_dict = {}
    for key, value in counts.items():
        reversed_key = key[::-1]
        prob_dict[reversed_key] = value / total
    return prob_dict
