# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QProg, CNOT, X


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1.")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'.")

    n = num_state_qubits
    if kind == "full":
        carry = 0
        a = list(range(1, n + 1))
        b = list(range(n + 1, 2 * n + 1))
        cout = 2 * n + 1
    else:
        a = list(range(n))
        b = list(range(n, 2 * n))
        cout = 2 * n if kind == "half" else None
        carry = 2 * n + 1 if kind == "half" else 2 * n

    program = QProg()

    def majority(x, y, z):
        program << CNOT(x, y)
        program << CNOT(x, z)
        program << X(x).control([z, y])

    def unmajority_add(x, y, z):
        program << X(x).control([z, y])
        program << CNOT(x, z)
        program << CNOT(z, y)

    majority(a[0], b[0], carry)
    for i in range(1, n):
        majority(a[i], b[i], a[i - 1])

    if cout is not None:
        program << CNOT(a[-1], cout)

    for i in range(n - 1, 0, -1):
        unmajority_add(a[i], b[i], a[i - 1])
    unmajority_add(a[0], b[0], carry)

    return program
