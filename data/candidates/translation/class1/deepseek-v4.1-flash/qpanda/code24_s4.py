# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

def dj_algorithm(oracle):
    qubits = oracle.qubits()
    n = len(qubits)
    qvm = CPUQVM()
    cbits = qvm.cAlloc_many(n - 1)
    qc = QCircuit()
    qc << X(qubits[-1])
    for q in qubits:
        qc << H(q)
    qc << oracle
    for q in qubits[:-1]:
        qc << H(q)
    for i in range(n - 1):
        qc << measure(qubits[i], cbits[i])
    prog = QProg() << qc
    qvm.run(prog, 1024)
    counts = qvm.result().get_counts()
    total = sum(counts.values())
    result = {}
    for key, value in counts.items():
        rev_key = key[::-1]
        result[rev_key] = value / total
    return result
