# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, CNOT, Toffoli


def _majority(circ, a, b, c):
    circ << CNOT(c, b)
    circ << CNOT(c, a)
    circ << Toffoli(a, b, c)


def _unmajority(circ, a, b, c):
    circ << Toffoli(a, b, c)
    circ << CNOT(c, a)
    circ << CNOT(a, b)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        cin = 0
        a = [1 + i for i in range(n)]
        b = [1 + n + i for i in range(n)]
        cout = 1 + 2 * n
        num_qubits = 2 * n + 2
    elif kind == "half":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        cout = 2 * n
        helper = 2 * n + 1
        num_qubits = 2 * n + 2
        cin = helper
    elif kind == "fixed":
        a = [i for i in range(n)]
        b = [n + i for i in range(n)]
        helper = 2 * n
        num_qubits = 2 * n + 1
        cin = helper
    else:
        raise ValueError("Unknown kind: {}".format(kind))

    circ = QCircuit(num_qubits)

    _majority(circ, cin, b[0], a[0])
    for i in range(n - 1):
        _majority(circ, a[i], b[i + 1], a[i + 1])

    if kind == "full" or kind == "half":
        circ << CNOT(a[n - 1], cout)

    for i in reversed(range(n - 1)):
        _unmajority(circ, a[i], b[i + 1], a[i + 1])
    _unmajority(circ, cin, b[0], a[0])

    prog = QProg()
    prog << circ
    return prog
