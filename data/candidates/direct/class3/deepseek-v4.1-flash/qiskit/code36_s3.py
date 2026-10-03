# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s):
    if isinstance(s, int):
        s = format(s, 'b')
    elif not isinstance(s, str):
        s = ''.join(str(bit) for bit in s)

    n = len(s)
    oracle = QuantumCircuit(n + 1)

    for i, bit in enumerate(s):
        if bit == '1':
            oracle.cx(i, n)

    return oracle
