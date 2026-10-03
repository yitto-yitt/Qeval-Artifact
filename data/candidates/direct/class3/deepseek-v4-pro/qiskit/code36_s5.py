# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    n = len(s)
    qc = QuantumCircuit(n + 1)
    for i, bit in enumerate(s):
        if int(bit):
            qc.cx(i, n)
    return qc
