# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    oracle = QuantumCircuit(len(s) + 1, name="BV Oracle")
    for qubit, bit in enumerate(reversed(s)):
        if bit == "1":
            oracle.cx(qubit, len(s))
    return oracle
