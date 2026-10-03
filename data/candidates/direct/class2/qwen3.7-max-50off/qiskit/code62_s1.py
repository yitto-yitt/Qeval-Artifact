# EVAL_META: task_id=62, framework=qiskit, class=2
from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    if isinstance(state, (int, float)):
        states = [int(state)]
        bases = [int(basis)]
    else:
        states = [int(s) for s in state]
        bases = [int(b) for b in basis]

    n = len(states)
    qc = QuantumCircuit(n)

    for i in range(n):
        if states[i] == 1:
            qc.x(i)
        if bases[i] == 1:
            qc.h(i)

    return qc
