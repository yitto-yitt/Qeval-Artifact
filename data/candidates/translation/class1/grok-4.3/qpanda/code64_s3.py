# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *
def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    qvm = CPUQVM()
    qvm.init_qvm()
    q_reg1 = qvm.qAlloc_many(n)
    q_reg2 = qvm.qAlloc_many(n)
    c_reg = qvm.cAlloc_many(n)
    circuit = QProg()
    for i in range(n):
        circuit << H(q_reg1[i])
    circuit << BARRIER(q_reg1 + q_reg2)
    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q_reg1[i], q_reg2[j])
        circuit << BARRIER(q_reg1 + q_reg2)
        for i in range(n):
            circuit << H(q_reg1[i])
    for i in range(n):
        circuit << Measure(q_reg1[i], c_reg[i])
    result = qvm.run_with_configuration(circuit, c_reg, 1024)
    return circuit
