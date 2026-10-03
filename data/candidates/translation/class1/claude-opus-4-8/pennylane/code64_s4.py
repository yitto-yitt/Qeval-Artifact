# EVAL_META: task_id=64, framework=pennylane, class=1
import pennylane as qml


def simons_algorithm(s):
    n = len(s)
    s = s[::-1]
    
    dev = qml.device('default.qubit', wires=2*n, shots=1024)
    
    @qml.qnode(dev)
    def circuit():
        for i in range(n):
            qml.Hadamard(wires=i)
        
        qml.Barrier(wires=range(2*n))
        
        for i in range(n):
            qml.CNOT(wires=[i, n+i])
        
        if "1" in s:
            idx = s.find("1")
            for j in range(n):
                if s[j] == "1":
                    qml.CNOT(wires=[idx, n+j])
            
            qml.Barrier(wires=range(2*n))
            
            for i in range(n):
                qml.Hadamard(wires=i)
        
        return qml.counts(wires=range(n))
    
    return circuit
