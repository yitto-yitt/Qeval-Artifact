# EVAL_META: task_id=64, framework=qpanda2, class=1
from pyqpanda import *

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    init_qvm()
    qubits = qAlloc_many(2 * n)
    cbits = cAlloc_many(n)
    q_reg1 = qubits[:n]
    q_reg2 = qubits[n:]
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
        for i in range(n):
            circuit << H(q_reg1[i])
    for i in range(n):
        circuit << Measure(q_reg1[i], cbits[i])
    return circuit
