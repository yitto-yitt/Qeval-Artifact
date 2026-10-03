# EVAL_META: task_id=64, framework=cirq, class=1
import cirq

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    q_reg1 = cirq.LineQubit.range(n)
    q_reg2 = cirq.LineQubit.range(n, 2 * n)
    
    circuit = cirq.Circuit()
    
    for q in q_reg1:
        circuit.append(cirq.H(q))
        
    for i in range(n):
        circuit.append(cirq.CNOT(q_reg1[i], q_reg2[i]))
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                circuit.append(cirq.CNOT(q_reg1[i], q_reg2[j]))
        for q in q_reg1:
            circuit.append(cirq.H(q))
            
    if n > 0:
        circuit.append(cirq.measure(*q_reg1, key='c'))
    
    return circuit
