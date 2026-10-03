# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis) -> QuantumCircuit:
    if not isinstance(state, (list, tuple, str)):
        states = [state]
        bases = [basis]
    else:
        states = list(state)
        bases = list(basis)
    
    n = len(states)
    qc = QuantumCircuit(n)
    for i in range(n):
        s = states[i]
        b = bases[i]
        
        if s in [1, '1', True]:
            qc.x(i)
        
        if b in [1, '1', 'X', 'x', 'H', 'h', True]:
            qc.h(i)
            
    return qc
