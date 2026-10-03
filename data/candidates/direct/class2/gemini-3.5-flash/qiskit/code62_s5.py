# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    if isinstance(state, str):
        states = [int(x) for x in state]
    elif isinstance(state, (int, float)):
        states = [int(state)]
    else:
        states = [int(x) for x in state]
        
    if isinstance(basis, str):
        if len(basis) == 1:
            bases = [basis]
        else:
            bases = list(basis)
    elif isinstance(basis, (int, float)):
        bases = [basis]
    else:
        bases = list(basis)
        
    n = len(states)
    qc = QuantumCircuit(n)
    for i in range(n):
        s = states[i]
        b = bases[i]
        if s == 1 or s == '1':
            qc.x(i)
        if b == 'X' or b == 1 or b == '1' or b == 'H' or b == 'x':
            qc.h(i)
    return qc
