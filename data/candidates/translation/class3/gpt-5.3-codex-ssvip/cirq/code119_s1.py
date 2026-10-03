# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in {"full", "half", "fixed"}:
        raise ValueError("kind must be one of 'full', 'half', or 'fixed'")

    n = int(num_state_qubits)
    if n <= 0:
        raise ValueError("num_state_qubits must be a positive integer")

    if kind == "full":
        total_qubits = 2 * n + 2
        cin_idx = 0
        a_start = 1
        b_start = 1 + n
        cout_idx = total_qubits - 1
    elif kind == "half":
        total_qubits = 2 * n + 2
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = total_qubits - 1
    else:  # fixed
        total_qubits = 2 * n + 1
        cin_idx = None
        a_start = 0
        b_start = n
        cout_idx = None

    q = cirq.LineQubit.range(total_qubits)
    a = [q[a_start + i] for i in range(n)]
    b = [q[b_start + i] for i in range(n)]
    cin = q[cin_idx] if cin_idx is not None else None
    cout = q[cout_idx] if cout_idx is not None else None

    circuit = cirq.Circuit()

    def majority(x, y, z):
        circuit.append(cirq.CNOT(z, y))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.CCX(x, y, z))

    def unmajority(x, y, z):
        circuit.append(cirq.CCX(x, y, z))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.CNOT(x, y))

    if kind == "full":
        majority(cin, b[0], a[0])
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], cout))
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        unmajority(cin, b[0], a[0])
    elif kind == "half":
        anc = q[-2]
        majority(anc, b[0], a[0])
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], cout))
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        unmajority(anc, b[0], a[0])
    else:  # fixed
        anc = q[-1]
        majority(anc, b[0], a[0])
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        unmajority(anc, b[0], a[0])

    return circuit
