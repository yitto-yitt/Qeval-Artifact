# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, CNOT, Toffoli


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    def maj(circ, a, b, c):
        circ << CNOT(c, b)
        circ << CNOT(c, a)
        circ << Toffoli(a, b, c)

    def uma(circ, a, b, c):
        circ << Toffoli(a, b, c)
        circ << CNOT(c, a)
        circ << CNOT(a, b)

    if kind == "full":
        # qubits: cin(1), a(n), b(n), cout(1)
        num_qubits = 2 * n + 2
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 1 + 2 * n
    elif kind == "half":
        # qubits: a(n), b(n), cout(1), helper(1)
        num_qubits = 2 * n + 2
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        cin = 2 * n + 1  # helper used as internal carry-in
    elif kind == "fixed":
        # qubits: a(n), b(n), helper(1)
        num_qubits = 2 * n + 1
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cin = 2 * n  # helper used as internal carry-in
        cout = None
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    circ = QCircuit(num_qubits)

    # forward MAJ chain
    maj(circ, cin, b[0], a[0])
    for i in range(1, n):
        maj(circ, a[i - 1], b[i], a[i])

    # carry out
    if cout is not None:
        circ << CNOT(a[n - 1], cout)

    # backward UMA chain
    for i in range(n - 1, 0, -1):
        uma(circ, a[i - 1], b[i], a[i])
    uma(circ, cin, b[0], a[0])

    prog = QProg()
    prog << circ
    return prog
