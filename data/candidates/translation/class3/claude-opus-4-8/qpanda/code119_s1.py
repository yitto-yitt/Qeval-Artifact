# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, CNOT, Toffoli


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    # Qubit layout depends on kind, matching Qiskit CDKMRippleCarryAdder
    if kind == "full":
        # cin, a[0..n-1], b[0..n-1], cout
        num_qubits = 2 * n + 2
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 2 * n + 1
    elif kind == "half":
        # a[0..n-1], b[0..n-1], cout, helper
        num_qubits = 2 * n + 2
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        cin = 2 * n + 1  # helper used as cin
    elif kind == "fixed":
        # a[0..n-1], b[0..n-1], helper
        num_qubits = 2 * n + 1
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        helper = 2 * n
        cin = helper
        cout = None
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def maj(circ, x, y, z):
        circ << CNOT(z, y)
        circ << CNOT(z, x)
        circ << Toffoli(x, y, z)

    def uma(circ, x, y, z):
        circ << Toffoli(x, y, z)
        circ << CNOT(z, x)
        circ << CNOT(x, y)

    circ = QCircuit(num_qubits)

    # MAJ chain
    maj(circ, cin, b[0], a[0])
    for i in range(1, n):
        maj(circ, a[i - 1], b[i], a[i])

    # carry out
    if kind in ("full", "half"):
        circ << CNOT(a[n - 1], cout)

    # UMA chain (reverse)
    for i in range(n - 1, 0, -1):
        uma(circ, a[i - 1], b[i], a[i])
    uma(circ, cin, b[0], a[0])

    prog = QProg()
    prog << circ
    return prog
