# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be one of 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    qvm = CPUQVM()
    qvm.init_qvm()

    n = num_state_qubits
    if kind == "full":
        total_qubits = 2 * n + 2
    elif kind == "half":
        total_qubits = 2 * n + 1
    else:  # fixed
        total_qubits = 2 * n

    q = qvm.qAlloc_many(total_qubits)
    prog = QProg()

    if kind == "full":
        cin = q[0]
        a = [q[1 + i] for i in range(n)]
        b = [q[1 + n + i] for i in range(n)]
        cout = q[-1]
    elif kind == "half":
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        cout = q[-1]
        cin = None
    else:  # fixed
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        cin = None
        cout = None

    def majority(c, bq, aq):
        return QCircuit() << CNOT(aq, bq) << CNOT(aq, c) << Toffoli(c, bq, aq)

    def unmajority(c, bq, aq):
        return QCircuit() << Toffoli(c, bq, aq) << CNOT(aq, c) << CNOT(c, bq)

    if kind == "full":
        prog << majority(cin, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(cin, b[0], a[0])

    elif kind == "half":
        anc = qvm.qAlloc()
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], cout)
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    else:  # fixed
        anc = qvm.qAlloc()
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    return prog
