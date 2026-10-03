# EVAL_META: task_id=119, framework=qpanda2, class=3
import atexit
from pyqpanda import *

_MAX_QUBITS = 64

machine = CPUQVM()
try:
    machine.set_configure(_MAX_QUBITS, _MAX_QUBITS)
except Exception:
    pass
machine.init_qvm()
q = machine.qAlloc_many(_MAX_QUBITS)


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("The number of state qubits must be at least 1.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    n = num_state_qubits

    if kind == "full":
        total_qubits = 2 * n + 2
        cin = q[0]
        a = [q[1 + i] for i in range(n)]
        b = [q[1 + n + i] for i in range(n)]
        cout = q[1 + 2 * n]
        carry_in = cin
    elif kind == "half":
        total_qubits = 2 * n + 2
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        cout = q[2 * n]
        carry_in = q[2 * n + 1]
    else:
        total_qubits = 2 * n + 1
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        cout = None
        carry_in = q[2 * n]

    if total_qubits > len(q):
        raise ValueError("Not enough globally allocated qubits for this adder size.")

    prog = QProg()

    def maj(qa, qb, qc):
        prog << CNOT(qa, qb)
        prog << CNOT(qa, qc)
        prog << Toffoli(qc, qb, qa)

    def uma(qa, qb, qc):
        prog << Toffoli(qc, qb, qa)
        prog << CNOT(qa, qc)
        prog << CNOT(qc, qb)

    maj(a[0], b[0], carry_in)
    for i in range(1, n):
        maj(a[i], b[i], a[i - 1])

    if cout is not None:
        prog << CNOT(a[n - 1], cout)

    for i in range(n - 1, 0, -1):
        uma(a[i], b[i], a[i - 1])
    uma(a[0], b[0], carry_in)

    return prog


atexit.register(machine.finalize)
