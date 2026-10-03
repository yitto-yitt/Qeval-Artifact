# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    machine = CPUQVM()
    machine.init_qvm()
    q_reg1 = machine.qAlloc_many(n)
    q_reg2 = machine.qAlloc_many(n)
    c_reg = machine.cAlloc_many(n)
    circuit = create_empty_circuit()
    q_all = q_reg1 + q_reg2
    for qubit in q_reg1:
        circuit << H(qubit)
    circuit << BARRIER(q_all)
    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q_reg1[i], q_reg2[j])
        circuit << BARRIER(q_all)
        for qubit in q_reg1:
            circuit << H(qubit)
    for i in range(n):
        circuit << Measure(q_reg1[i], c_reg[i])
    return circuit
