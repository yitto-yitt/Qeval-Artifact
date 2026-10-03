# EVAL_META: task_id=36, framework=qiskit, class=3
from qiskit import QuantumCircuit


def bv_function(s):
    """
    Design a Bernstein-Vazirani oracle from a bitstring.

    The oracle implements f(x) = s · x (mod 2) using CNOT gates
    from each input qubit i (where s[i] == '1') to an ancilla qubit.

    Args:
        s (str): A bitstring representing the secret string (e.g., "1011").

    Returns:
        QuantumCircuit: The BV oracle circuit with len(s) input qubits
                        and 1 ancilla qubit.
    """
    n = len(s)
    oracle = QuantumCircuit(n + 1)
    for i in range(n):
        if s[i] == '1':
            oracle.cx(i, n)
    return oracle
