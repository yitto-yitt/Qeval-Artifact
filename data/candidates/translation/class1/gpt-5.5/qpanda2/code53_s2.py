# EVAL_META: task_id=53, framework=qpanda2, class=1
import builtins
from pyqpanda import *

def xor_gate(a, b):
    shots = 1024
    n = 8

    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n)
    cbits = qvm.cAlloc_many(n)

    pos_of_qubit = {}
    for i in range(n):
        cal_prog = QProg()
        cal_prog << X(qubits[i])
        cal_prog << measure_all(qubits, cbits)
        cal_counts = qvm.run_with_configuration(cal_prog, cbits, 1)
        cal_key = next(iter(cal_counts.keys()))
        pos_of_qubit[i] = cal_key.index("1")

    prog = QProg()
    for i in range(n):
        if (a >> i) & 1:
            prog << X(qubits[i])
    for i in range(n):
        if (b >> i) & 1:
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)

    counts = qvm.run_with_configuration(prog, cbits, shots)
    qvm.finalize()

    transformed = {}
    for key, value in counts.items():
        out = ["0"] * n
        for i in range(n):
            out[n - 1 - i] = key[pos_of_qubit[i]]
        out_key = "".join(out)
        transformed[out_key] = transformed.get(out_key, 0) + value

    total = builtins.sum(transformed.values())
    return {key: value / total for key, value in transformed.items()}
