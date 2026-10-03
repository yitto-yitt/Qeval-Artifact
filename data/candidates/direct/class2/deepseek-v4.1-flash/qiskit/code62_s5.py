# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    if isinstance(state, int):
        state = [state]
    if isinstance(basis, int):
        basis = [basis]
    n = len(state)
    qc = QuantumCircuit(n)
    for i in range(n):
        s = state[i]
        b = basis[i]
        if s == 1 or s == '1' or s is True:
            qc.x(i)
        if b == 1 or b == '1' or b is True:
            qc.h(i)
    return qc
