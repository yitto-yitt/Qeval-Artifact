# EVAL_META: task_id=36, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(20)

def bv_function(s):
    n = len(s)
    prog = QProg()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << CNOT(qubits[index], qubits[n])
    return prog

machine.finalize()
