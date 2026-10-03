# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, qalloc, calloc, H, CNOT, Measure


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    q1 = qalloc(n)
    q2 = qalloc(n)
    c = calloc(n)

    circuit = QCircuit()

    for qubit in q1:
        circuit << H(qubit)

    for i in range(n):
        circuit << CNOT(q1[i], q2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q1[i], q2[j])

        for qubit in q1:
            circuit << H(qubit)

    for i in range(n):
        circuit << Measure(q1[i], c[i])

    return circuit
