# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def bv_algorithm(s):
    n = len(s)
    qvm = CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)
    prog = QProg()
    ancilla = n
    prog << X(qubits[ancilla])
    for i in range(n + 1):
        prog << H(qubits[i])
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(qubits[index], qubits[ancilla])
    for i in range(n):
        prog << H(qubits[i])
    for i in range(n):
        prog << Measure(qubits[i], cbits[i])
    counts = qvm.run_with_configuration(prog, cbits, shots=1)
    total_shots = builtins.sum(counts.values())
    bitstrings = []
    for k, v in counts.items():
        bitstrings.extend([k] * v)
    return [bitstrings, counts]
