# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        num_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(num_qubits)
        cin = qubits[0]
        a = qubits[1:1 + n]
        b = qubits[1 + n:1 + 2 * n]
        cout = qubits[1 + 2 * n]
        carry_in = cin
    elif kind == "half":
        num_qubits = 2 * n + 2
        qubits = cirq.LineQubit.range(num_qubits)
        a = qubits[0:n]
        b = qubits[n:2 * n]
        cout = qubits[2 * n]
        carry_in = qubits[2 * n + 1]
    elif kind == "fixed":
        num_qubits = 2 * n + 1
        qubits = cirq.LineQubit.range(num_qubits)
        a = qubits[0:n]
        b = qubits[n:2 * n]
        cout = None
        carry_in = qubits[2 * n]
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    def maj(q0, q1, q2):
        return [
            cirq.CNOT(q2, q1),
            cirq.CNOT(q2, q0),
            cirq.TOFFOLI(q0, q1, q2),
        ]

    def uma(q0, q1, q2):
        return [
            cirq.TOFFOLI(q0, q1, q2),
            cirq.CNOT(q2, q0),
            cirq.CNOT(q0, q1),
        ]

    ops = []

    if n > 0:
        ops.extend(maj(carry_in, b[0], a[0]))

        for j in range(n - 1):
            ops.extend(maj(a[j], b[j + 1], a[j + 1]))

        if cout is not None:
            ops.append(cirq.CNOT(a[n - 1], cout))

        for j in reversed(range(n - 1)):
            ops.extend(uma(a[j], b[j + 1], a[j + 1]))

        ops.extend(uma(carry_in, b[0], a[0]))

    return cirq.Circuit(ops)
