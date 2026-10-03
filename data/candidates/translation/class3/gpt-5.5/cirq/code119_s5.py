# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if num_state_qubits < 1:
        raise ValueError("num_state_qubits must be at least 1")
    if kind not in ("full", "half", "fixed"):
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    n = num_state_qubits

    if kind == "full":
        qubits = cirq.LineQubit.range(2 * n + 2)
        carry = qubits[0]
        a = qubits[1 : n + 1]
        b = qubits[n + 1 : 2 * n + 1]
        cout = qubits[2 * n + 1]
    elif kind == "half":
        qubits = cirq.LineQubit.range(2 * n + 2)
        a = qubits[0:n]
        b = qubits[n : 2 * n]
        cout = qubits[2 * n]
        carry = qubits[2 * n + 1]
    else:
        qubits = cirq.LineQubit.range(2 * n + 1)
        a = qubits[0:n]
        b = qubits[n : 2 * n]
        carry = qubits[2 * n]
        cout = None

    def maj(aq, bq, cq):
        return [
            cirq.CNOT(aq, bq),
            cirq.CNOT(aq, cq),
            cirq.TOFFOLI(cq, bq, aq),
        ]

    def uma(aq, bq, cq):
        return [
            cirq.TOFFOLI(cq, bq, aq),
            cirq.CNOT(aq, cq),
            cirq.CNOT(cq, bq),
        ]

    ops = []
    ops.extend(maj(a[0], b[0], carry))

    for i in range(n - 1):
        ops.extend(maj(a[i + 1], b[i + 1], a[i]))

    if kind != "fixed":
        ops.append(cirq.CNOT(a[n - 1], cout))

    for i in reversed(range(n - 1)):
        ops.extend(uma(a[i + 1], b[i + 1], a[i]))

    ops.extend(uma(a[0], b[0], carry))

    return cirq.Circuit(ops)
