# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def _maj(a, b, c):
    return [cirq.CNOT(c, b), cirq.CNOT(c, a), cirq.CCX(a, b, c)]


def _uma(a, b, c):
    return [cirq.CCX(a, b, c), cirq.CNOT(c, a), cirq.CNOT(a, b)]


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    if kind == "full":
        # qubits: cin, a[0..n-1], b[0..n-1], cout
        cin = cirq.LineQubit(0)
        a = [cirq.LineQubit(1 + i) for i in range(n)]
        b = [cirq.LineQubit(1 + n + i) for i in range(n)]
        cout = cirq.LineQubit(1 + 2 * n)

        circuit = cirq.Circuit()

        circuit.append(_maj(cin, b[0], a[0]))
        for i in range(1, n):
            circuit.append(_maj(a[i - 1], b[i], a[i]))

        circuit.append(cirq.CNOT(a[n - 1], cout))

        for i in range(n - 1, 0, -1):
            circuit.append(_uma(a[i - 1], b[i], a[i]))
        circuit.append(_uma(cin, b[0], a[0]))

        return circuit

    elif kind == "half":
        # qubits: a[0..n-1], b[0..n-1], cout, helper
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        cout = cirq.LineQubit(2 * n)
        helper = cirq.LineQubit(2 * n + 1)

        circuit = cirq.Circuit()

        circuit.append(_maj(helper, b[0], a[0]))
        for i in range(1, n):
            circuit.append(_maj(a[i - 1], b[i], a[i]))

        circuit.append(cirq.CNOT(a[n - 1], cout))

        for i in range(n - 1, 0, -1):
            circuit.append(_uma(a[i - 1], b[i], a[i]))
        circuit.append(_uma(helper, b[0], a[0]))

        return circuit

    elif kind == "fixed":
        # qubits: a[0..n-1], b[0..n-1], helper
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        helper = cirq.LineQubit(2 * n)

        circuit = cirq.Circuit()

        if n == 1:
            circuit.append(cirq.CNOT(a[0], b[0]))
            return circuit

        circuit.append(_maj(helper, b[0], a[0]))
        for i in range(1, n):
            circuit.append(_maj(a[i - 1], b[i], a[i]))

        for i in range(n - 1, 0, -1):
            circuit.append(_uma(a[i - 1], b[i], a[i]))
        circuit.append(_uma(helper, b[0], a[0]))

        return circuit

    else:
        raise ValueError(f"Unknown kind: {kind}")
