# EVAL_META: task_id=62, framework=qiskit, class=2

from qiskit import QuantumCircuit

def bb84_senders_circuit(state, basis):
    n = len(state)
    qc = QuantumCircuit(n, n)
    
    for i in range(n):
        if state[i] == 1:
            qc.x(i)
            
        if basis[i] == 1:
            qc.h(i)
            
    return qc
