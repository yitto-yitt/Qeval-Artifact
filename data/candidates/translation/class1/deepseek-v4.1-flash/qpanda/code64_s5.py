# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, Measure, BARRIER

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = [Qubit(i, "reg1") for i in range(n)]
    q_reg2 = [Qubit(n + i, "reg2") for i in range(n)]
    c_reg = [CBit(i, "c") for i in range(n)]
    circuit = QCircuit()
    for q in q_reg1:
        circuit << H(q)
    circuit << BARRIER(q_reg1)
    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q_reg1[i], q_reg2[j])
        circuit << BARRIER(q_reg1)
        for q in q_reg1:
            circuit << H(q)
    for i in range(n):
        circuit << Measure(q_reg1[i], c_reg[i])
    return circuit
