# EVAL_META: task_id=119, framework=qpanda, class=3
from pyqpanda3.core import *


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = int(num_state_qubits)
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    if kind == "full":
        num_qubits = 2 * n + 2
    elif kind == "half":
        num_qubits = 2 * n + 2
    else:
        num_qubits = 2 * n + 1

    machine = CPUQVM()
    try:
        machine.init_qvm()
    except Exception:
        pass
    q = machine.qAlloc_many(num_qubits)

    circuit = QCircuit()

    def _append(gate):
        nonlocal circuit
        circuit << gate

    def _cx(control, target):
        return CNOT(control, target)

    def _ccx(control1, control2, target):
        if "Toffoli" in globals():
            return Toffoli(control1, control2, target)
        return CCX(control1, control2, target)

    def _maj(carry, b_qubit, a_qubit):
        _append(_cx(a_qubit, b_qubit))
        _append(_cx(a_qubit, carry))
        _append(_ccx(carry, b_qubit, a_qubit))

    def _uma(carry, b_qubit, a_qubit):
        _append(_ccx(carry, b_qubit, a_qubit))
        _append(_cx(a_qubit, carry))
        _append(_cx(carry, b_qubit))

    if kind == "full":
        cin = q[0]
        a = [q[1 + i] for i in range(n)]
        b = [q[1 + n + i] for i in range(n)]
        cout = q[2 * n + 1]

        _maj(cin, b[0], a[0])
        for i in range(1, n):
            _maj(a[i - 1], b[i], a[i])
        _append(_cx(a[n - 1], cout))
        for i in range(n - 1, 0, -1):
            _uma(a[i - 1], b[i], a[i])
        _uma(cin, b[0], a[0])

    elif kind == "half":
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        cout = q[2 * n]
        helper = q[2 * n + 1]

        _maj(helper, b[0], a[0])
        for i in range(1, n):
            _maj(a[i - 1], b[i], a[i])
        _append(_cx(a[n - 1], cout))
        for i in range(n - 1, 0, -1):
            _uma(a[i - 1], b[i], a[i])
        _uma(helper, b[0], a[0])

    else:
        a = [q[i] for i in range(n)]
        b = [q[n + i] for i in range(n)]
        helper = q[2 * n]

        _maj(helper, b[0], a[0])
        for i in range(1, n):
            _maj(a[i - 1], b[i], a[i])
        for i in range(n - 1, 0, -1):
            _uma(a[i - 1], b[i], a[i])
        _uma(helper, b[0], a[0])

    try:
        circuit._machine = machine
        circuit._qubits = q
    except Exception:
        pass

    return circuit
