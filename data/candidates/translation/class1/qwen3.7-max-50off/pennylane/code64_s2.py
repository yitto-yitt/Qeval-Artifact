# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml

def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    with qml.tape.QuantumTape() as tape:
        for i in range(n):
            qml.Hadamard(wires=i)
            
        for i in range(n):
            qml.CNOT(wires=[i, i + n])
            
        if "1" in s:
            i = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[i, j + n])
                    
            for k in range(n):
                qml.Hadamard(wires=k)
                
        qml.sample(wires=list(range(n)))
        
    return tape
