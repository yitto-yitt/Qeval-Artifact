# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit


def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(n, n)
    for i, bit in enumerate(s):
        if bit == "1":
            qc.x(i)
    qc.measure(range(n), range(n))
    qc.cregs[0].name = "c"
    return qc
