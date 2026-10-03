# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
from qiskit.quantum_info import Operator

def dj_algorithm(oracle):
    n = oracle.num_qubits
    mat = Operator(oracle).data
    
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
            
        qml.QubitUnitary(mat, wires=list(range(n))[::-1])
        
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=list(range(n-2, -1, -1)))
        
    probs = circuit()
    res = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            bs = format(i, f'0{n-1}b')
            res[bs] = p
    return res
