# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s: str) -> QuantumCircuit:
    """
    Creates a Bernstein-Vazirani oracle for the given bitstring s.
    The oracle uses n + 1 qubits, where n is the length of s.
    The first n qubits are the input register, and the last qubit (index n) is the target.
    """
    n = len(s)
    qc = QuantumCircuit(n + 1)
    
    # Reverse the string to match Qiskit's little-endian qubit ordering
    s_reversed = s[::-1]
    for i in range(n):
        if s_reversed[i] == '1':
            qc.cx(i, n)
            
    return qc
