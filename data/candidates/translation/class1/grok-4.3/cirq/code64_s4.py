# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = [cirq.LineQubit(i) for i in range(n)]
    q_reg2 = [cirq.LineQubit(n + i) for i in range(n)]
    circuit = cirq.Circuit()
    circuit.append(cirq.H.on_each(q_reg1))
    for i in range(n):
        circuit.append(cirq.CNOT(q_reg1[i], q_reg2[i]))
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(q_reg1[i], q_reg2[j]))
        circuit.append(cirq.H.on_each(q_reg1))
    circuit.append(cirq.measure(*q_reg1, key="c"))
    return circuit
