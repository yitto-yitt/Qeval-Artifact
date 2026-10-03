# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, QProg, CPUQVM, H, X, measure

def dj_algorithm(oracle):
    if isinstance(oracle, QCircuit):
        n = oracle.qubit_num()
    else:
        n = oracle.num_qubits

    qc = QCircuit(n)
    qc << X(n - 1)
    for q in range(n):
        qc << H(q)
    qc << oracle
    for q in range(n):
        qc << H(q)

    prog = QProg()
    prog << qc
    for q in range(n - 1):
        prog << measure(q, q)

    qvm = CPUQVM()
    qvm.run(prog, 10000)
    counts = qvm.result().get_counts()

    total = sum(counts.values())
    return {key: value / total for key, value in counts.items()}
