# EVAL_META: task_id=64, framework=cirq, class=1
import cirq


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    reg1 = [cirq.NamedQubit(f"reg1_{i}") for i in range(n)]
    reg2 = [cirq.NamedQubit(f"reg2_{i}") for i in range(n)]
    circuit = cirq.Circuit()
    circuit.append([cirq.H(q) for q in reg1])
    for i in range(n):
        circuit.append(cirq.CNOT(reg1[i], reg2[i]))
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(reg1[i], reg2[j]))
        circuit.append([cirq.H(q) for q in reg1])
    circuit.append(cirq.measure(*reg1, key='c'))
    return circuit
