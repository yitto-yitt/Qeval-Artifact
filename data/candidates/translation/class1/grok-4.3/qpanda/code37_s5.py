# EVAL_META: task_id=37, framework=qpanda, class=1
from pyqpanda3.core import CPUQVM, QProg, H, X, CNOT, measure
def bv_algorithm(s):
    n = len(s)
    machine = CPUQVM()
    machine.init_qvm()
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    prog = QProg()
    ancilla = n
    prog << X(q[ancilla])
    prog << [H(q[i]) for i in range(n + 1)]
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(q[index], q[ancilla])
    prog << [H(q[i]) for i in range(n)]
    prog << measure(q[:n], c)
    result = machine.run_with_configuration(prog, c, shots=1)
    bitstrings = list(result.keys())
    return [bitstrings, result]
