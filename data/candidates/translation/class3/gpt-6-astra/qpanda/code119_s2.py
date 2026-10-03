# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import QProg, CNOT, Toffoli


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
        carry_out = 2 * n + 1
    else:
        a = list(range(n))
        b = list(range(n, 2 * n))
        carry_out = 2 * n if kind == "half" else None
        carry = 2 * n + 1 if kind == "half" else 2 * n

    program = QProg()

    for i in range(n):
        previous_carry = carry if i == 0 else a[i - 1]
        program << CNOT(a[i], b[i])
        program << CNOT(a[i], previous_carry)
        program << Toffoli(previous_carry, b[i], a[i])

    if carry_out is not None:
        program << CNOT(a[-1], carry_out)

    for i in reversed(range(n)):
        previous_carry = carry if i == 0 else a[i - 1]
        program << Toffoli(previous_carry, b[i], a[i])
        program << CNOT(a[i], previous_carry)
        program << CNOT(previous_carry, b[i])

    return program
