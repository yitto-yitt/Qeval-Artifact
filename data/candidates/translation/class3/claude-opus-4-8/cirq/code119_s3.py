# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def _maj(circuit, a, b, c):
    circuit.append(cirq.CNOT(c, b))
    circuit.append(cirq.CNOT(c, a))
    circuit.append(cirq.CCX(a, b, c))


def _uma(circuit, a, b, c):
    circuit.append(cirq.CCX(a, b, c))
    circuit.append(cirq.CNOT(c, a))
    circuit.append(cirq.CNOT(a, b))


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if n < 1:
        raise ValueError("num_state_qubits must be >= 1")

    if kind == "full":
        # qubits: cin, a[0..n-1] interleaved, b, cout per Qiskit ordering
        # Qiskit register order for 'full': cin(1), a(n), b(n), cout(1)
        cin = cirq.LineQubit(0)
        a = [cirq.LineQubit(1 + i) for i in range(n)]
        b = [cirq.LineQubit(1 + n + i) for i in range(n)]
        cout = cirq.LineQubit(1 + 2 * n)
        circuit = cirq.Circuit()

        _maj(circuit, cin, b[0], a[0])
        for i in range(1, n):
            _maj(circuit, a[i - 1], b[i], a[i])

        circuit.append(cirq.CNOT(a[n - 1], cout))

        for i in range(n - 1, 0, -1):
            _uma(circuit, a[i - 1], b[i], a[i])
        _uma(circuit, cin, b[0], a[0])

        return circuit

    elif kind == "half":
        # Qiskit register order for 'half': a(n), b(n), cout(1)
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        cout = cirq.LineQubit(2 * n)
        helper = cirq.LineQubit(2 * n + 1)
        circuit = cirq.Circuit()

        _maj(circuit, helper, b[0], a[0])
        for i in range(1, n):
            _maj(circuit, a[i - 1], b[i], a[i])

        circuit.append(cirq.CNOT(a[n - 1], cout))

        for i in range(n - 1, 0, -1):
            _uma(circuit, a[i - 1], b[i], a[i])
        _uma(circuit, helper, b[0], a[0])

        return circuit

    elif kind == "fixed":
        # Qiskit register order for 'fixed': a(n), b(n)
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        helper = cirq.LineQubit(2 * n)
        circuit = cirq.Circuit()

        _maj(circuit, helper, b[0], a[0])
        for i in range(1, n):
            _maj(circuit, a[i - 1], b[i], a[i])

        for i in range(n - 1, 0, -1):
            _uma(circuit, a[i - 1], b[i], a[i])
        _uma(circuit, helper, b[0], a[0])

        return circuit

    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
