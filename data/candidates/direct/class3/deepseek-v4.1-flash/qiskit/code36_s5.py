# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s):
    if isinstance(s, int):
        s = format(s, 'b')
    elif isinstance(s, (list, tuple)):
        s = ''.join(str(int(b)) for b in s)
    else:
        s = str(s)

    n = len(s)
    qc = QuantumCircuit(n + 1, name="BV Oracle")
    for i, bit in enumerate(s):
        if bit == '1':
            qc.cx(i, n)
    return qc
