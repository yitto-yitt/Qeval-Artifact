# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    n = num_state_qubits
    if kind == 'full':
        num_qubits = 2 * n + 1
    elif kind in ('half', 'fixed'):
        num_qubits = 2 * n
    else:
        raise ValueError("kind must be 'full', 'half', or 'fixed'")

    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()

    if kind == 'full':
        a = qubits[:n]
        b = qubits[n:2*n]
        c = qubits[2*n]

        # MAJ chain
        for i in range(n):
            circuit.append([cirq.CNOT(c, b[i]),
                            cirq.CNOT(c, a[i]),
                            cirq.CCX(a[i], b[i], c)])

        circuit.append(cirq.CNOT(a[n-1], c))

        # UMA chain
        for i in reversed(range(n)):
            circuit.append([cirq.CCX(a[i], b[i], c),
                            cirq.CNOT(c, a[i]),
                            cirq.CNOT(a[i], b[i])])
    else:  # half or fixed
        if n == 1:
            circuit.append(cirq.CNOT(qubits[0], qubits[1]))
        else:
            a = qubits[:n]
            b = qubits[n:]

            # MAJ chain
            for i in range(n - 1):
                circuit.append([cirq.CNOT(a[i+1], b[i]),
                                cirq.CNOT(a[i+1], a[i]),
                                cirq.CCX(a[i], b[i], a[i+1])])
            circuit.append([cirq.CNOT(a[0], b[n-1]),
                            cirq.CNOT(a[0], a[n-1]),
                            cirq.CCX(a[n-1], b[n-1], a[0])])

            circuit.append(cirq.CNOT(a[n-1], a[0]))

            # UMA chain
            for i in reversed(range(n - 1)):
                circuit.append([cirq.CCX(a[i], b[i], a[i+1]),
                                cirq.CNOT(a[i+1], a[i]),
                                cirq.CNOT(a[i], b[i])])
            circuit.append([cirq.CCX(a[n-1], b[n-1], a[0]),
                            cirq.CNOT(a[0], a[n-1]),
                            cirq.CNOT(a[n-1], b[n-1])])

    return circuit

