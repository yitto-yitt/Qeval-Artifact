# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3.core import QCircuit, Qubit, CBit, H, CNOT, measure, barrier

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = [Qubit(i) for i in range(n)]
    q_reg2 = [Qubit(n + i) for i in range(n)]
    c_reg = [CBit(i) for i in range(n)]
    circuit = QCircuit()
    
    for q in q_reg1:
        circuit << H(q)
    
    all_qubits = q_reg1 + q_reg2
    circuit << barrier(all_qubits)
    
    for i in range(n):
        circuit << CNOT(q_reg1[i], q_reg2[i])
    
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit << CNOT(q_reg1[i], q_reg2[j])
        circuit << barrier(all_qubits)
        for q in q_reg1:
            circuit << H(q)
    
    for i in range(n):
        circuit << measure(q_reg1[i], c_reg[i])
    
    return circuit
