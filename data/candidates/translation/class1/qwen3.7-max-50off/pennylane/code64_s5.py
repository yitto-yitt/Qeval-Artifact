# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    ops = []
    
    for i in range(n):
        ops.append(qml.Hadamard(wires=i))
        
    ops.append(qml.Barrier(wires=list(range(2 * n))))
    
    for i in range(n):
        ops.append(qml.CNOT(wires=[i, n + i]))
        
    if "1" in s:
        i = s.find("1")
        for j in range(n):
            if s[j] == "1":
                ops.append(qml.CNOT(wires=[i, n + j]))
        ops.append(qml.Barrier(wires=list(range(2 * n))))
        for k in range(n):
            ops.append(qml.Hadamard(wires=k))
            
    measurements = [qml.sample(wires=i) for i in range(n)]
    
    tape = qml.tape.QuantumScript(ops, measurements)
    return tape
