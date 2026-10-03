# EVAL_META: task_id=64, framework=qpanda, class=1
from pyqpanda3 import QuantumCircuit, QuantumRegister, ClassicalRegister

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    q_reg1 = QuantumRegister(n, "reg1")
    q_reg2 = QuantumRegister(n, "reg2")
    c_reg = ClassicalRegister(n, "c")
    circuit = QuantumCircuit(q_reg1, q_reg2, c_reg)
    
    for i in range(n):
        circuit.h(q_reg1[i])
        
    circuit.barrier()
    
    for i in range(n):
        circuit.cx(q_reg1[i], q_reg2[i])
        
    if "1" in s:
        idx = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.cx(q_reg1[idx], q_reg2[j])
        circuit.barrier()
        for i in range(n):
            circuit.h(q_reg1[i])
            
    circuit.measure(q_reg1, c_reg)
    return circuit
