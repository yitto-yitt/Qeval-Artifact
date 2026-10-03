# EVAL_META: task_id=119, framework=pennylane, class=3
import pennylane as qml


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    ops = []

    def maj(carry, b, a):
        ops.append(qml.CNOT(wires=[a, b]))
        ops.append(qml.CNOT(wires=[a, carry]))
        ops.append(qml.Toffoli(wires=[carry, b, a]))

    def uma(carry, b, a):
        ops.append(qml.Toffoli(wires=[carry, b, a]))
        ops.append(qml.CNOT(wires=[a, carry]))
        ops.append(qml.CNOT(wires=[carry, b]))

    if kind == "full":
        cin = 0
        a_start = 1
        b_start = 1 + n
        cout = 1 + 2 * n

        maj(cin, b_start, a_start)
        for i in range(1, n):
            maj(a_start + i - 1, b_start + i, a_start + i)

        ops.append(qml.CNOT(wires=[a_start + n - 1, cout]))

        for i in range(n - 1, 0, -1):
            uma(a_start + i - 1, b_start + i, a_start + i)
        uma(cin, b_start, a_start)

    elif kind == "half":
        a_start = 0
        b_start = n
        cout = 2 * n
        helper = 2 * n + 1

        maj(helper, b_start, a_start)
        for i in range(1, n):
            maj(a_start + i - 1, b_start + i, a_start + i)

        ops.append(qml.CNOT(wires=[a_start + n - 1, cout]))

        for i in range(n - 1, 0, -1):
            uma(a_start + i - 1, b_start + i, a_start + i)
        uma(helper, b_start, a_start)

    elif kind == "fixed":
        a_start = 0
        b_start = n
        helper = 2 * n

        maj(helper, b_start, a_start)
        for i in range(1, n):
            maj(a_start + i - 1, b_start + i, a_start + i)

        for i in range(n - 1, 0, -1):
            uma(a_start + i - 1, b_start + i, a_start + i)
        uma(helper, b_start, a_start)

    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    return qml.tape.QuantumScript(ops, [])
