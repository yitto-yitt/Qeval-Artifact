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
        if (a & (1 << i)):
            prog << X(qubits[i])
    for i in range(8):
        if (b & (1 << i)):
            prog << X(qubits[i])
    prog << measure_all(qubits, cbits)
    shots = 1024
    counts = qvm.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    dist = {}
    for key, value in counts.items():
        bitstring = format(key, '08b')
        dist[bitstring] = value / total
    return dist
