# EVAL_META: task_id=24, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def dj_algorithm(oracle):
    n = oracle.num_qubits
    machine = CPUQVM()
    machine.init_qvm()
    qubits = machine.qAlloc_many(n)
    cbits = machine.cAlloc_many(n - 1)
    prog = QProg()
    prog << X(qubits[n - 1])
    for i in range(n):
        prog << H(qubits[i])
    prog << oracle
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n - 1):
        prog << Measure(qubits[i], cbits[i])
    shots = 1024
    counts = machine.run_with_configuration(prog, cbits, shots)
    total = builtins.sum(counts.values())
    return {key: value / total for key, value in counts.items()}
