# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be >= 1")

    machine = CPUQVM()
    machine.init_qvm()

    n = num_state_qubits
    if kind == "full":
        total_qubits = 2 * n + 2
        cin_idx = 0
        a_start = 1
        b_start = 1 + n
        cout_idx = total_qubits - 1
    elif kind == "half":
        total_qubits = 2 * n + 1
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = total_qubits - 1
    else:  # fixed
        total_qubits = 2 * n
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = None

    q = machine.qAlloc_many(total_qubits)
    prog = QProg()

    def majority(c, b, a):
        circ = QCircuit()
        circ << CNOT(a, b)
        circ << CNOT(a, c)
        circ << Toffoli(c, b, a)
        return circ

    def unmajority(c, b, a):
        circ = QCircuit()
        circ << Toffoli(c, b, a)
        circ << CNOT(a, c)
        circ << CNOT(c, b)
        return circ

    a = [q[a_start + i] for i in range(n)]
    b = [q[b_start + i] for i in range(n)]

    if kind == "full":
        c0 = q[cin_idx]
        prog << majority(c0, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], q[cout_idx])
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(c0, b[0], a[0])

    elif kind == "half":
        anc = q[cout_idx]
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        prog << CNOT(a[n - 1], anc)
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    else:  # fixed
        anc = machine.qAlloc()
        prog << majority(anc, b[0], a[0])
        for i in range(1, n):
            prog << majority(a[i - 1], b[i], a[i])
        for i in range(n - 1, 0, -1):
            prog << unmajority(a[i - 1], b[i], a[i])
        prog << unmajority(anc, b[0], a[0])

    return prog
