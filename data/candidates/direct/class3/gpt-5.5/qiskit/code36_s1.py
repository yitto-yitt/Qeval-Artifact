# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    s = str(s)
    n = len(s)
    oracle = QuantumCircuit(n + 1, name="BV oracle")
    for i, bit in enumerate(reversed(s)):
        if bit == "1":
            oracle.cx(i, n)
    return oracle
