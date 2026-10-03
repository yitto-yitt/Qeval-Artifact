# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    n = len(state)
    qc = QuantumCircuit(n)
    for i in range(n):
        s = state[i]
        b = basis[i]
        if isinstance(s, str):
            s = int(s)
        if isinstance(b, str):
            b = 1 if b.upper() == 'X' else 0
        if s == 1:
            qc.x(i)
        if b == 1:
            qc.h(i)
    return qc
