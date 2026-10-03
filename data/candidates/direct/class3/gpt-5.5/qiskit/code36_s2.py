# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    qc = QuantumCircuit(len(s) + 1)
    for index, bit in enumerate(reversed(s)):
        if bit == "1":
            qc.cx(index, len(s))
    return qc
