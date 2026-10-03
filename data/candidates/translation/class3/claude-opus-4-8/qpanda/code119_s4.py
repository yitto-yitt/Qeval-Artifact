# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QCircuit, QProg, X, CNOT, Toffoli

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    def _maj(circ, a, b, c):
        circ << CNOT(c, b)
        circ << CNOT(c, a)
        circ << Toffoli(a, b, c)

    def _uma(circ, a, b, c):
        circ << Toffoli(a, b, c)
        circ << CNOT(c, a)
        circ << CNOT(a, b)

    if kind == "full":
        num_qubits = 2 * n + 2
        cin = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
    elif kind == "half":
        num_qubits = 2 * n + 1
        cin = None
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = 2 * n
    elif kind == "fixed":
        num_qubits = 2 * n
        cin = None
        a = list(range(0, n))
        b = list(range(n, 2 * n))
        cout = None
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    circ = QCircuit(num_qubits)

    helper = num_qubits if kind != "full" else None
    if kind != "full":
        circ = QCircuit(num_qubits + 1)
        helper = num_qubits

    carries = []
    if kind == "full":
        first_carry = cin
    else:
        first_carry = helper

    _maj(circ, a[0], b[0], first_carry)
    for i in range(1, n):
        _maj(circ, a[i], b[i], a[i - 1] if False else a[i - 1])

    circ2 = QCircuit(num_qubits if kind == "full" else num_qubits + 1)
    prev = first_carry
    for i in range(n):
        _maj(circ2, a[i], b[i], prev)
        prev = a[i]

    if kind == "full":
        circ2 << CNOT(a[n - 1], cout)
    elif kind == "half":
        circ2 << CNOT(a[n - 1], cout)

    for i in reversed(range(n)):
        prev = first_carry if i == 0 else a[i - 1]
        _uma(circ2, a[i], b[i], prev)

    prog = QProg()
    prog << circ2

    from pyqpanda3.core import CPUQVM
    qvm = CPUQVM()
    qvm.run(prog, 0)
    return prog
