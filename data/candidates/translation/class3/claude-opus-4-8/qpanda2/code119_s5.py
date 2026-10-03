# EVAL_META: task_id=119, framework=qpanda2, class=3
from pyqpanda import *

machine = CPUQVM()
machine.init_qvm()
qubits = machine.qAlloc_many(64)


def _maj(a, b, c):
    prog = QProg()
    prog << CNOT(c, b) << CNOT(c, a) << Toffoli(a, b, c)
    return prog


def _uma(a, b, c):
    prog = QProg()
    prog << Toffoli(a, b, c) << CNOT(c, a) << CNOT(a, b)
    return prog


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    prog = QProg()

    if kind == 'full':
        cin = qubits[0]
        a = [qubits[1 + i] for i in range(n)]
        b = [qubits[1 + n + i] for i in range(n)]
        cout = qubits[1 + 2 * n]

        prog << _maj(cin, b[0], a[0])
        for i in range(1, n):
            prog << _maj(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            prog << _uma(a[i - 1], b[i], a[i])
        prog << _uma(cin, b[0], a[0])

    elif kind == 'half':
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        cout = qubits[2 * n]
        helper = qubits[2 * n + 1]

        prog << _maj(helper, b[0], a[0])
        for i in range(1, n):
            prog << _maj(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            prog << _uma(a[i - 1], b[i], a[i])
        prog << _uma(helper, b[0], a[0])

    else:  # fixed
        a = [qubits[i] for i in range(n)]
        b = [qubits[n + i] for i in range(n)]
        helper = qubits[2 * n]

        if n == 1:
            prog << CNOT(a[0], b[0])
        else:
            prog << _maj(helper, b[0], a[0])
            for i in range(1, n):
                prog << _maj(a[i - 1], b[i], a[i])
            for i in range(n - 1, 0, -1):
                prog << _uma(a[i - 1], b[i], a[i])
            prog << _uma(helper, b[0], a[0])

    return prog


if __name__ == "__main__":
    p = create_ripple_carry_adder_circuit(2, 'full')
    print(p)
    machine.finalize()
