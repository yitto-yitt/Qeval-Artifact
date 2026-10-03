# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits

    def maj(a, b, c):
        return [cirq.CNOT(c, b), cirq.CNOT(c, a), cirq.CCX(a, b, c)]

    def uma(a, b, c):
        return [cirq.CCX(a, b, c), cirq.CNOT(c, a), cirq.CNOT(a, b)]

    if kind == "full":
        cin = cirq.LineQubit.range(1)[0]
        a = cirq.LineQubit.range(1, 1 + n)
        b = cirq.LineQubit.range(1 + n, 1 + 2 * n)
        cout = cirq.LineQubit(1 + 2 * n)
        num_qubits = 2 + 2 * n
    elif kind == "half":
        a = cirq.LineQubit.range(0, n)
        b = cirq.LineQubit.range(n, 2 * n)
        cout = cirq.LineQubit(2 * n)
        helper = cirq.LineQubit(2 * n + 1)
        cin = helper
        num_qubits = 2 * n + 2
    elif kind == "fixed":
        a = cirq.LineQubit.range(0, n)
        b = cirq.LineQubit.range(n, 2 * n)
        helper = cirq.LineQubit(2 * n)
        cin = helper
        cout = None
        num_qubits = 2 * n + 1
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    ops = []

    # forward MAJ chain
    ops += maj(cin, b[0], a[0])
    for i in range(1, n):
        ops += maj(a[i - 1], b[i], a[i])

    # carry out
    if cout is not None:
        ops.append(cirq.CNOT(a[n - 1], cout))

    # backward UMA chain
    for i in range(n - 1, 0, -1):
        ops += uma(a[i - 1], b[i], a[i])
    ops += uma(cin, b[0], a[0])

    circuit = cirq.Circuit(ops)
    all_qubits = cirq.LineQubit.range(num_qubits)
    for q in all_qubits:
        if q not in circuit.all_qubits():
            circuit.append(cirq.I(q))
    return circuit
