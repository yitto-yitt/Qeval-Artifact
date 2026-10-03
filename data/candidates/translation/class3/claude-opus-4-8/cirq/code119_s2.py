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
        cin = [cirq.LineQubit(0)]
        a = [cirq.LineQubit(1 + i) for i in range(n)]
        b = [cirq.LineQubit(1 + n + i) for i in range(n)]
        cout = [cirq.LineQubit(1 + 2 * n)]
        num_qubits = 2 + 2 * n
    elif kind == "half":
        cin = None
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        cout = [cirq.LineQubit(2 * n)]
        num_qubits = 1 + 2 * n
    elif kind == "fixed":
        cin = None
        a = [cirq.LineQubit(i) for i in range(n)]
        b = [cirq.LineQubit(n + i) for i in range(n)]
        cout = None
        num_qubits = 2 * n
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    circuit = cirq.Circuit()

    # ancilla helper carry
    helper = cirq.LineQubit(num_qubits)

    if kind == "full":
        carry_in = cin[0]
    else:
        carry_in = helper

    # MAJ chain
    maj(circuit, carry_in, b[0], a[0])
    for i in range(1, n):
        maj(circuit, a[i - 1], b[i], a[i])

    # carry out
    if cout is not None:
        circuit.append(cirq.CNOT(a[n - 1], cout[0]))

    # UMA chain
    for i in range(n - 1, 0, -1):
        uma(circuit, a[i - 1], b[i], a[i])
    uma(circuit, carry_in, b[0], a[0])

    return circuit
