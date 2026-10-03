# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit
def bb84_senders_circuit(state, basis):
    n = len(state)
    qc = QuantumCircuit(n)
    for i in range(n):
        s = int(state[i])
        b = int(basis[i])
        if b == 0:
            if s == 1:
                qc.x(i)
        else:
            if s == 1:
                qc.x(i)
            qc.h(i)
    return qc
