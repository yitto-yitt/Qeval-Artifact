# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s: str) -> cirq.Circuit:
    n = len(s)
    s = s[::-1]

    qubits_reg1 = cirq.LineQubit.range(n)
    qubits_reg2 = cirq.LineQubit.range(n, 2 * n)

    circuit = cirq.Circuit()

    # Apply Hadamard to all reg1 qubits
    circuit.append(cirq.H.on_each(*qubits_reg1))

    # Barrier (no-op in Cirq, just for visual separation)
    circuit.append(cirq.I.on_each(*qubits_reg1, *qubits_reg2))

    # Apply CNOT from reg1 to reg2
    for i in range(n):
        circuit.append(cirq.CNOT(qubits_reg1[i], qubits_reg2[i]))

    # Oracle for secret string s
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(qubits_reg1[i], qubits_reg2[j]))

        # Barrier (no-op)
        circuit.append(cirq.I.on_each(*qubits_reg1, *qubits_reg2))

        # Apply Hadamard to all reg1 qubits
        circuit.append(cirq.H.on_each(*qubits_reg1))

    # Measure reg1 into classical register (simulated via measurement gate)
    circuit.append(cirq.measure(*qubits_reg1, key="c"))

    return circuit
