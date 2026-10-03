# EVAL_META: task_id=36, framework=qpanda2, class=3
import pyqpanda as pq

machine = pq.CPUQVM()
machine.init_qvm()
_global_qubits = machine.qAlloc_many(64)

def bv_function(s):
    n = len(s)
    qubits = _global_qubits[: n + 1]
    prog = pq.QProg()
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qubits[index], qubits[n])
    return prog

machine.finalize()
