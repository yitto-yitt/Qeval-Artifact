# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s: str) -> cirq.Circuit:
    n = len(s)
    s_rev = s[::-1]
    q_reg1 = [cirq.LineQubit(i) for i in range(n)]
    q_reg2 = [cirq.LineQubit(i + n) for i in range(n)]
    c_reg = [cirq.LineQubit(i + 2 * n) for i in range(n)]

    circuit = cirq.Circuit()

    # Apply Hadamard gates to reg1
    circuit.append([cirq.H(q) for q in q_reg1])

    # Barrier is not strictly needed in Cirq, but we can add a moment separator
    # We'll just proceed to the next operations.

    # CNOT gates from reg1 to reg2
    circuit.append([cirq.CNOT(q_reg1[i], q_reg2[i]) for i in range(n)])

    if "1" in s_rev:
        i = s_rev.find("1")
        for j in range(n):
            if s_rev[j] == "1":
                circuit.append(cirq.CNOT(q_reg1[i], q_reg2[j]))

        # Another barrier equivalent
        # Apply Hadamard gates to reg1 again
        circuit.append([cirq.H(q) for q in q_reg1])

    # Measure reg1 into classical registers
    circuit.append([cirq.measure(q_reg1[i], c_reg[i]) for i in range(n)])

    return circuit
