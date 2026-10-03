# EVAL_META: task_id=119, framework=cirq, class=3
import cirq

def create_ripple_carry_adder_circuit(num_state_qubits, kind):
    if kind == "full":
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n + 2)
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry = qubits[2 * n:]
        circuit = cirq.Circuit()
        circuit.append(cirq.CNOT(carry[0], b[0]))
        circuit.append(cirq.CCX(a[0], b[0], carry[1]))
        for i in range(1, n):
            circuit.append(cirq.CCX(carry[i], b[i], carry[i + 1]))
            circuit.append(cirq.CCX(a[i], b[i], carry[i + 1]))
        for i in range(n - 1, 0, -1):
            circuit.append(cirq.CNOT(a[i], b[i]))
            circuit.append(cirq.CCX(carry[i], b[i], carry[i + 1]))
            circuit.append(cirq.CCX(a[i], b[i], carry[i + 1]))
        circuit.append(cirq.CNOT(a[0], b[0]))
        circuit.append(cirq.CNOT(carry[0], b[0]))
        circuit.append(cirq.CNOT(carry[n], carry[n - 1]))
        return circuit
    elif kind == "half":
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n + 1)
        a = qubits[:n]
        b = qubits[n:2 * n]
        carry = qubits[2 * n:]
        circuit = cirq.Circuit()
        circuit.append(cirq.CCX(a[0], b[0], carry[0]))
        for i in range(1, n):
            circuit.append(cirq.CCX(carry[i - 1], b[i], carry[0]))
            circuit.append(cirq.CCX(a[i], b[i], carry[0]))
        for i in range(n - 1, 0, -1):
            circuit.append(cirq.CNOT(a[i], b[i]))
            circuit.append(cirq.CCX(carry[i - 1], b[i], carry[0]))
            circuit.append(cirq.CCX(a[i], b[i], carry[0]))
        circuit.append(cirq.CNOT(a[0], b[0]))
        return circuit
    else:
        n = num_state_qubits
        qubits = cirq.LineQubit.range(2 * n)
        a = qubits[:n]
        b = qubits[n:]
        circuit = cirq.Circuit()
        for i in range(n):
            circuit.append(cirq.CNOT(a[i], b[i]))
        return circuit
