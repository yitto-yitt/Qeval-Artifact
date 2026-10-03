# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    def maj(circuit, a, b, c):
        circuit.append(cirq.CNOT(c, b))
        circuit.append(cirq.CNOT(c, a))
        circuit.append(cirq.CCX(a, b, c))

    def uma(circuit, a, b, c):
        circuit.append(cirq.CCX(a, b, c))
        circuit.append(cirq.CNOT(c, a))
        circuit.append(cirq.CNOT(a, b))

    if kind == "full":
        cin = cirq.LineQubit.range(1)
        a = cirq.LineQubit.range(1, 1 + n)
        b = cirq.LineQubit.range(1 + n, 1 + 2 * n)
        cout = cirq.LineQubit(1 + 2 * n)
        cin_q = cin[0]

        circuit = cirq.Circuit()
        maj(circuit, cin_q, b[0], a[0])
        for i in range(1, n):
            maj(circuit, a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], cout))
        for i in range(n - 1, 0, -1):
            uma(circuit, a[i - 1], b[i], a[i])
        uma(circuit, cin_q, b[0], a[0])
        return circuit

    elif kind == "half":
        a = cirq.LineQubit.range(0, n)
        b = cirq.LineQubit.range(n, 2 * n)
        cout = cirq.LineQubit(2 * n)
        helper = cirq.LineQubit(2 * n + 1)

        circuit = cirq.Circuit()
        maj(circuit, helper, b[0], a[0])
        for i in range(1, n):
            maj(circuit, a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], cout))
        for i in range(n - 1, 0, -1):
            uma(circuit, a[i - 1], b[i], a[i])
        uma(circuit, helper, b[0], a[0])
        return circuit

    elif kind == "fixed":
        a = cirq.LineQubit.range(0, n)
        b = cirq.LineQubit.range(n, 2 * n)
        helper = cirq.LineQubit(2 * n)

        circuit = cirq.Circuit()
        maj(circuit, helper, b[0], a[0])
        for i in range(1, n):
            maj(circuit, a[i - 1], b[i], a[i])
        for i in range(n - 1, 0, -1):
            uma(circuit, a[i - 1], b[i], a[i])
        uma(circuit, helper, b[0], a[0])
        return circuit

    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")
