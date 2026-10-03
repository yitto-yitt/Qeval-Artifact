# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    n = len(s)
    qc = QuantumCircuit(n + 1)  # n input qubits + 1 ancilla qubit
    
    # Apply X gate to ancilla qubit (initialize to |1>)
    qc.x(n)
    
    # Apply CNOT gates based on the secret string s
    for i in range(n):
        if s[i] == '1':
            qc.cx(i, n)
    
    return qc
