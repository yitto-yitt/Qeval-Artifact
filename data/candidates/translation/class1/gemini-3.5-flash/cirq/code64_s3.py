# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = [cirq.NamedQubit(f"reg1_{i}") for i in range(n)]
    q_reg2 = [cirq.NamedQubit(f"reg2_{i}") for i in range(n)]

    circuit = cirq.Circuit()

    # H on q_reg1
    circuit.append(cirq.H.on_each(*q_reg1))

    # CX from q_reg1 to q_reg2
    for k in range(n):
        circuit.append(cirq.CX(q_reg1[k], q_reg2[k]))

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CX(q_reg1[i], q_reg2[j]))
        circuit.append(cirq.H.on_each(*q_reg1))

    # Measure q_reg1
    circuit.append(cirq.measure(*q_reg1, key="c"))

    return circuit
