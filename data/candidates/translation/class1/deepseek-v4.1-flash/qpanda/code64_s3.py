# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, Measure, BARRIER

def simons_algorithm(s):
    n = len(s)
    s_rev = s[::-1]
    reg1 = [Qubit(i) for i in range(n)]
    reg2 = [Qubit(i + n) for i in range(n)]
    c_reg = [CBit(i) for i in range(n)]
    circuit = QCircuit()
    for q in reg1:
        circuit << H(q)
    all_qubits = reg1 + reg2
    circuit << BARRIER(all_qubits)
    for i in range(n):
        circuit << CNOT(reg1[i], reg2[i])
    if "1" in s_rev:
        i_ctrl = s_rev.find("1")
        for j in range(n):
            if s_rev[j] == "1":
                circuit << CNOT(reg1[i_ctrl], reg2[j])
        circuit << BARRIER(all_qubits)
        for q in reg1:
            circuit << H(q)
    for i in range(n):
        circuit << Measure(reg1[i], c_reg[i])
    return circuit
