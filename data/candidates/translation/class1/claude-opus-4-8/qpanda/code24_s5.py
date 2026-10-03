# EVAL_META: task_id=24, framework=qpanda, class=1
from pyqpanda3.core import QProg, QCircuit, CPUQVM, H, X, measure
from pyqpanda3.core import quantum_info

def dj_algorithm(oracle):
    n = oracle.num_qubits

    qc = QCircuit(n)
    qc << X(n - 1)
    for i in range(n):
        qc << H(i)
    qc << oracle
    for i in range(n):
        qc << H(i)

    prog = QProg()
    prog << qc
    for i in range(n - 1):
        prog << measure(i, i)

    qvm = CPUQVM()
    result = qvm.run(prog, 100000)
    counts = result.get_counts()

    fixed = {}
    for key, value in counts.items():
        k = key[-(n - 1):] if n - 1 > 0 else ""
        fixed[k] = fixed.get(k, 0) + value

    total = sum(fixed.values())
    return {key: value / total for key, value in fixed.items()}
