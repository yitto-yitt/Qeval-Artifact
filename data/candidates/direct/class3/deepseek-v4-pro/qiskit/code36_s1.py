# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit

def bv_function(s):
    """
    Construct a Bernstein-Vazirani oracle for a given hidden bitstring s.

    Args:
        s (str): Hidden bitstring (e.g., '1010').

    Returns:
        QuantumCircuit: The oracle circuit with len(s)+1 qubits.
    """
    n = len(s)
    qc = QuantumCircuit(n + 1)
    for i, bit in enumerate(s):
        if bit == '1':
            qc.cx(i, n)
    return qc
