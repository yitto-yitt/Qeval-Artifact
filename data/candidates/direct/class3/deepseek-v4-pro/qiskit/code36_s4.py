# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    """Create a Bernstein-Vazirani oracle for the secret bitstring s."""
    n = len(s)
    qc = QuantumCircuit(n + 1)

    for qubit, bit in enumerate(reversed(s)):
        if bit == '1':
            qc.cx(qubit, n)

    return qc
