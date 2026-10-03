# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *
import builtins

def bv_algorithm(s):
    n = len(s)
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    meas = machine.cAlloc_many(n)
    ancilla = n
    prog = QProg()
    prog << X(q[ancilla])
    for qubit in q:
        prog << H(qubit)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << Measure(q[i], meas[i])
    shots = 1
    result = machine.run_with_configuration(prog, shots)
    bitstrings = []
    for bs, count in result.items():
        bitstrings.extend([bs] * count)
    machine.finalize()
    return [bitstrings, result]
