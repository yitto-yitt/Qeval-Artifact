# EVAL_META: task_id=37, framework=pennylane, class=1
import pennylane as qml

def bv_algorithm(s):
    n = len(s)
    dev = qml.device("default.qubit", wires=n + 1, shots=1)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n)
        for i in range(n + 1):
            qml.Hadamard(wires=i)
            
        for index, bit in enumerate(reversed(s)):
            if bit == "1":
                qml.CNOT(wires=[index, n])
                
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.sample(wires=range(n))
    
    result = circuit()
    if hasattr(result, "flatten"):
        flat_res = result.flatten()
    else:
        flat_res = result
    bitstrings = ["".join(str(int(b)) for b in flat_res[::-1])]
    
    return [bitstrings, result]
