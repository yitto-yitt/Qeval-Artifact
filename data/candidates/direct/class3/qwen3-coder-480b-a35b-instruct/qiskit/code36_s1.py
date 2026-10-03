# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s):
    n = len(s)
    oracle = QuantumCircuit(n + 1)
    
    for i in range(n):
        if s[i] == '1':
            oracle.cx(i, n)
            
    return oracle
