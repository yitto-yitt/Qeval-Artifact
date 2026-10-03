# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def _maj(prog, a, b, c):
    prog << CNOT(c, b)
    prog << CNOT(c, a)
    prog << Toffoli(a, b, c)


def _uma(prog, a, b, c):
    prog << Toffoli(a, b, c)
    prog << CNOT(c, a)
    prog << CNOT(a, b)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    prog = QProg()

    if kind == 'full':
        cin = qubits[0]
        a = [qubits[1 + i] for i in range(n)]
        b = [qubits[1 + n + i] for i in range(n)]
        cout = qubits[1 + 2 * n]

        _maj(prog, cin, b[0], a[0])
        for i in range(1, n):
            _maj(prog, a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            _uma(prog, a[i - 1], b[i], a[i])
        _uma(prog, cin, b[0], a[0])

    elif kind == 'half':
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        cout = qubits[2 * n]
        helper = qubits[2 * n + 1]

        _maj(prog, helper, b[0], a[0])
        for i in range(1, n):
            _maj(prog, a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            _uma(prog, a[i - 1], b[i], a[i])
        _uma(prog, helper, b[0], a[0])

    elif kind == 'fixed':
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        helper = qubits[2 * n]

        _maj(prog, helper, b[0], a[0])
        for i in range(1, n):
            _maj(prog, a[i - 1], b[i], a[i])
        for i in range(n - 1, 0, -1):
            _uma(prog, a[i - 1], b[i], a[i])
        _uma(prog, helper, b[0], a[0])

    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    return prog
