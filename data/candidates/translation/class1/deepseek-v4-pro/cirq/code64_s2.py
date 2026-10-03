# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = cirq.LineQubit.range(n)
    q_reg2 = cirq.LineQubit.range(n, 2 * n)
    c_reg = cirq.LineQubit.range(2 * n, 3 * n)

    circuit = cirq.Circuit()

    # Apply Hadamard to first register
    circuit.append(cirq.H.on_each(*q_reg1))

    # Barrier (no-op in Cirq, but we can add a moment separator if desired; omit for semantics)
    # CNOT between registers
    for i in range(n):
        circuit.append(cirq.CNOT(q_reg1[i], q_reg2[i]))

    if "1" in s:
        idx = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(q_reg1[idx], q_reg2[j]))

        # Barrier (no-op)
        # Hadamard on first register
        circuit.append(cirq.H.on_each(*q_reg1))

    # Measure first register into classical register
    circuit.append(cirq.measure(*q_reg1, key="c"))

    return circuit
