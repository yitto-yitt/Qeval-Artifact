# EVAL_META: task_id=119, framework=cirq, class=3
import cirq


def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind not in {"full", "half", "fixed"}:
        raise ValueError("kind must be one of {'full', 'half', 'fixed'}")

    n = int(num_state_qubits)
    if n <= 0:
        raise ValueError("num_state_qubits must be a positive integer")

    if kind == "full":
        total_qubits = 2 * n + 2
        cin = 0
        a_start = 1
        b_start = 1 + n
        cout = 2 * n + 1
    elif kind == "half":
        total_qubits = 2 * n + 1
        cin = None
        a_start = 0
        b_start = n
        cout = 2 * n
    else:  # fixed
        total_qubits = 2 * n
        cin = None
        a_start = 0
        b_start = n
        cout = None

    q = cirq.LineQubit.range(total_qubits)
    a = [q[a_start + i] for i in range(n)]
    b = [q[b_start + i] for i in range(n)]

    circuit = cirq.Circuit()

    def majority(x, y, z):
        circuit.append(cirq.CNOT(z, y))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.TOFFOLI(x, y, z))

    def unmajority(x, y, z):
        circuit.append(cirq.TOFFOLI(x, y, z))
        circuit.append(cirq.CNOT(z, x))
        circuit.append(cirq.CNOT(x, y))

    if kind == "full":
        c = q[cin]
        majority(c, b[0], a[0])
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], q[cout]))
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        unmajority(c, b[0], a[0])

    elif kind == "half":
        anc = q[cout]
        circuit.append(cirq.CNOT(a[0], b[0]))
        circuit.append(cirq.CNOT(a[0], anc))
        circuit.append(cirq.TOFFOLI(anc, b[0], a[0]))
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        circuit.append(cirq.CNOT(a[n - 1], anc))
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        circuit.append(cirq.TOFFOLI(anc, b[0], a[0]))
        circuit.append(cirq.CNOT(a[0], anc))
        circuit.append(cirq.CNOT(a[0], b[0]))

    else:  # fixed
        anc = cirq.NamedQubit("ancilla")
        circuit.append(cirq.CNOT(a[0], b[0]))
        circuit.append(cirq.CNOT(a[0], anc))
        circuit.append(cirq.TOFFOLI(anc, b[0], a[0]))
        for i in range(1, n):
            majority(a[i - 1], b[i], a[i])
        for i in reversed(range(1, n)):
            unmajority(a[i - 1], b[i], a[i])
        circuit.append(cirq.TOFFOLI(anc, b[0], a[0]))
        circuit.append(cirq.CNOT(a[0], anc))
        circuit.append(cirq.CNOT(a[0], b[0]))

    return circuit
