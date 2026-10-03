# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq
import builtins


def bv_algorithm(s):
    n = len(s)
    machine = pq.CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    prog = pq.QProg()
    ancilla = n
    prog.insert(pq.X(q[ancilla]))
    for i in range(n + 1):
        prog.insert(pq.H(q[i]))
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog.insert(pq.CNOT(q[index], q[ancilla]))
    for i in range(n):
        prog.insert(pq.H(q[i]))
    for i in range(n):
        prog.insert(pq.Measure(q[i], c[i]))
    result = machine.run_with_configuration(prog, c, shots=1)
    bitstrings = []
    for k, v in result.items():
        bitstrings.extend([k] * v)
    return [bitstrings, result]
