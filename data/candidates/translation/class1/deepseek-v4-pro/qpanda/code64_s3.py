# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import *


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]

    init_quantum_machine(QMachineType.CPU)
    q_reg1 = qAlloc_many(n)
    q_reg2 = qAlloc_many(n)
    c_reg = cAlloc_many(n)

    circuit = QCircuit()

    for i in range(n):
        circuit << H(q_reg1[i])

    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])

    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q_reg1[i], q_reg2[j])

        for k in range(n):
            circuit << H(q_reg1[k])

    for i in range(n):
        circuit << Measure(q_reg1[i], c_reg[i])

    return circuit
