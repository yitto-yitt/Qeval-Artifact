# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s: str) -> QuantumCircuit:
    n = len(s)
    qc = QuantumCircuit(n + 1)
    s_reversed = s[::-1]
    for i in range(n):
        if s_reversed[i] == '1':
            qc.cx(i, n)
    return qc
