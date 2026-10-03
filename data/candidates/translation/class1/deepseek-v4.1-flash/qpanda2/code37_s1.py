# EVAL_META: task_id=37, framework=qpanda2, class=1
from pyqpanda import *

def bv_algorithm(s):
    n = len(s)
    machine = init_quantum_machine(QMachineType.CPU)
    q = machine.qAlloc_many(n + 1)
    c = machine.cAlloc_many(n)
    prog = QProg()
    prog << X(q[n])
    for i in range(n + 1):
        prog << H(q[i])
    for i, bit in enumerate(reversed(s)):
        if bit == '1':
            prog << CNOT(q[i], q[n])
    for i in range(n):
        prog << H(q[i])
    for i in range(n):
        prog << Measure(q[i], c[i])
    result = machine.run_with_configuration(prog, c, shots=1)
    bitstring = None
    for key, count in result.items():
        if count > 0:
            if isinstance(key, str):
                bitstring = key.zfill(n)
            else:
                bitstring = format(key, '0{}b'.format(n))
            break
    if bitstring is None:
        bitstring = '0' * n
    bitstrings = [bitstring]
    return [bitstrings, result]
