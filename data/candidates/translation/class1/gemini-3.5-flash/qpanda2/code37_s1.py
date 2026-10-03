# EVAL_META: task_id=37, framework=qpanda2, class=1
import pyqpanda as pq


def bv_algorithm(s):
    n = len(s)
    qvm = pq.CPUQVM()
    qvm.init_qvm()
    qubits = qvm.qAlloc_many(n + 1)
    cbits = qvm.cAlloc_many(n)

    prog = pq.QProg()
    prog << pq.X(qubits[n])

    for i in range(n + 1):
        prog << pq.H(qubits[i])

    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            prog << pq.CNOT(qubits[index], qubits[n])

    for i in range(n):
        prog << pq.H(qubits[i])

    for i in range(n):
        prog << pq.Measure(qubits[i], cbits[i])

    result = qvm.run_with_configuration(prog, cbits, 1)
    bitstrings = list(result.keys())

    return [bitstrings, result]
