# EVAL_META: task_id=64, framework=qiskit, class=1
from qiskit import QuantumCircuit, ClassicalRegister


def simons_algorithm(s):
    n = len(s)
    c = ClassicalRegister(n, "c")
    qc = QuantumCircuit(n, n)
    qc.add_register(c)
    for i, bit in enumerate(s):
        if bit == "1":
            qc.x(i)
    qc.measure(range(n), c)
    return qc
