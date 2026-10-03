# EVAL_META: task_id=24, framework=pennylane, class=1
import pennylane as qml
import numpy as np
from qiskit.quantum_info import Operator

def dj_algorithm(oracle):
    n = oracle.num_qubits
    U = Operator(oracle).data
    
    dev = qml.device("default.qubit", wires=n)
    
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=n-1)
        for i in range(n):
            qml.Hadamard(wires=i)
            
        qml.QubitUnitary(U, wires=range(n))
        
        for i in range(n):
            qml.Hadamard(wires=i)
            
        return qml.probs(wires=range(n-1))
        
    probs = circuit()
    
    result_dict = {}
    for i, p in enumerate(probs):
        if p > 1e-9:
            bitstring = format(i, f'0{n-1}b')
            result_dict[bitstring] = p
            
    return result_dict
