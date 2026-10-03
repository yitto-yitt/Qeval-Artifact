# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, Measure, BARRIER

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    reg1 = [Qubit(i) for i in range(n)]
    reg2 = [Qubit(i + n) for i in range(n)]
    c = [CBit(i) for i in range(n)]
    circuit = QCircuit()
    for q in reg1:
        circuit << H(q)
    circuit << BARRIER(reg1 + reg2)
    for i in range(n):
        circuit << CNOT(reg1[i], reg2[i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(reg1[i], reg2[j])
        circuit << BARRIER(reg1 + reg2)
        for q in reg1:
            circuit << H(q)
    for i in range(n):
        circuit << Measure(reg1[i], c[i])
    return circuit
