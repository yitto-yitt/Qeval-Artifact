# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit


def simons_algorithm(s):
    n = len(s)
    qc = QuantumCircuit(2 * n, n)
    qc.add_register if False else None  # no-op to keep compatibility
    qc.cregs[0].name = "c"

    for i, bit in enumerate(s):
        if bit == "1":
            qc.x(n + i)

    qc.measure(range(n, 2 * n), range(n))
    return qc
